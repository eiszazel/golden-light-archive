#!/usr/bin/env python3
"""Ingest blog.remilia.org posts into markdown files using Firecrawl.

This script expects /tmp/remilia-blog-map.json to exist from:
  firecrawl map https://blog.remilia.org/ --wait --limit 200 --json --pretty -o /tmp/remilia-blog-map.json

It reads FIRECRAWL_API_KEY from the environment or ~/.hermes/.env.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "remilia-blog"
MAP_PATH = Path("/tmp/remilia-blog-map.json")
API_URL = "https://api.firecrawl.dev/v1/scrape"

EXCLUDE_PATH_BITS = (
    "/author/",
    "/tag/",
    "/about",
    "/contact",
    "/privacy",
    "/contribute",
)


def read_firecrawl_key() -> str:
    if os.environ.get("FIRECRAWL_API_KEY"):
        return os.environ["FIRECRAWL_API_KEY"].strip()
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for line in env_path.read_text(errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("export FIRECRAWL_API_KEY=") or line.startswith("FIRECRAWL_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("FIRECRAWL_API_KEY not found in environment or ~/.hermes/.env")


def slug_from_url(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", slug).strip("-").lower()
    return slug or "index"


def load_post_links() -> list[dict[str, Any]]:
    data = json.loads(MAP_PATH.read_text())
    links = data.get("data", {}).get("links", [])
    posts = []
    seen = set()
    for item in links:
        if isinstance(item, str):
            item = {"url": item}
        url = item.get("url")
        if not url or not url.startswith("https://blog.remilia.org"):
            continue
        if url.rstrip("/") == "https://blog.remilia.org":
            continue
        if any(bit in url for bit in EXCLUDE_PATH_BITS):
            continue
        if url in seen:
            continue
        seen.add(url)
        posts.append(item)
    return posts


def scrape(api_key: str, url: str) -> dict[str, Any]:
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "maxAge": 0,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def clean_markdown(markdown: str) -> str:
    md = markdown.replace("\r\n", "\n")
    # Remove common footer/challenge clutter if Firecrawl includes it.
    md = re.sub(r"\nChecking your Browser.*$", "", md, flags=re.DOTALL | re.IGNORECASE)
    md = re.sub(r"\nWallet · Privy.*$", "", md, flags=re.DOTALL)
    md = re.sub(r"\nStart writing\n\n20\d{2} .*$", "", md, flags=re.DOTALL)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    return md.strip() + "\n"


def extract_title(markdown: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return fallback.strip() or fallback_from_slug(fallback)


def fallback_from_slug(text: str) -> str:
    return text.replace("-", " ").replace("_", " ").title()


def frontmatter(title: str, source_url: str, scraped_at: str, original_title=None) -> str:
    safe_title = title.replace('"', '\\"')
    safe_orig = (original_title or title).replace('"', '\\"')
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        'source: "Remilia Corporation Blog"\n'
        f'url: "{source_url}"\n'
        f'scraped_at: "{scraped_at}"\n'
        f'original_map_title: "{safe_orig}"\n'
        "---\n\n"
    )


def main() -> int:
    api_key = read_firecrawl_key()
    posts = load_post_links()
    OUT_DIR.mkdir(exist_ok=True)
    scraped_at = datetime.now(timezone.utc).isoformat()
    metadata = []
    failures = []

    print(f"Discovered {len(posts)} blog.remilia.org post URLs")
    for i, item in enumerate(posts, 1):
        url = item["url"]
        slug = slug_from_url(url)
        out_path = OUT_DIR / f"{slug}.md"
        print(f"[{i:02d}/{len(posts)}] {slug}")
        try:
            data = scrape(api_key, url)
            if not data.get("success"):
                raise RuntimeError(json.dumps(data)[:500])
            payload = data.get("data") or {}
            markdown = clean_markdown(payload.get("markdown") or "")
            if len(markdown) < 200:
                raise RuntimeError(f"suspiciously short markdown: {len(markdown)} chars")
            title = extract_title(markdown, item.get("title") or fallback_from_slug(slug))
            out_path.write_text(frontmatter(title, url, scraped_at, item.get("title")) + markdown, encoding="utf-8")
            metadata.append({
                "slug": slug,
                "title": title,
                "url": url,
                "path": str(out_path.relative_to(ROOT)),
                "chars": len(markdown),
                "source": "blog.remilia.org",
                "scraped_at": scraped_at,
            })
            print(f"  saved {out_path.relative_to(ROOT)} ({len(markdown):,} chars)")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            failures.append({"url": url, "slug": slug, "error": f"HTTP {exc.code}: {body}"})
            print(f"  failed HTTP {exc.code}")
        except Exception as exc:
            failures.append({"url": url, "slug": slug, "error": str(exc)})
            print(f"  failed {exc}")
        time.sleep(0.75)

    (ROOT / "remilia-blog-metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if failures:
        (ROOT / "remilia-blog-failures.json").write_text(json.dumps(failures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        fail_path = ROOT / "remilia-blog-failures.json"
        if fail_path.exists():
            fail_path.unlink()

    print(f"\nExtracted {len(metadata)} posts")
    print(f"Failures: {len(failures)}")
    print(f"Output: {OUT_DIR}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
