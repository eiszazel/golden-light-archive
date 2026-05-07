#!/usr/bin/env python3
"""Fill missing Paragraph / Golden Light posts discovered from the Charlotte Fang archive pages.

Reads FIRECRAWL_API_KEY from env or ~/.hermes/.env.
Does not store the API key in repo files.
"""

import json
import os
import re
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API_URL = "https://api.firecrawl.dev/v1/scrape"

POSTS = [
    {"url":"https://paragraph.com/@charlemagnefang/a-people-s-history-of-hot-pot-gp","title":"A People’s History of Hot Pot [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/a-profile-on-milady-maker-s-charlotte-fang-gp","title":"A Profile on Milady Maker's Charlotte Fang [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/admin-reveal-i-said-i-m-just-a-vessel-bro","title":"Admin Reveal: I said I'm just a vessel bro"},
    {"url":"https://paragraph.com/@charlemagnefang/alignment-fraud-cthulhu-hears-no-protest","title":"Alignment Fraud: Cthulhu Hears No Protest"},
    {"url":"https://paragraph.com/@charlemagnefang/angelicism01-collected-commentaries-on-milady","title":"Angelicism01: Collected Commentaries on Milady"},
    {"url":"https://paragraph.com/@charlemagnefang/auction-core-gp","title":"Auction Core [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/bonkler-critical-notes","title":"Bonkler: Critical Notes"},
    {"url":"https://paragraph.com/@charlemagnefang/can-what-s-playing-milady-make-it-to-level-2","title":"Can what's playing Milady make it to Level-2?"},
    {"url":"https://paragraph.com/@charlemagnefang/cancel-miya-to-me-or-i-ll-fucking-kill-you","title":"Cancel Miya to me or I’ll fucking kill you"},
    {"url":"https://paragraph.com/@charlemagnefang/crypto-and-its-discontents-hello-web3-entryists","title":"Crypto and its Discontents: Hello Web3 Entryists"},
    {"url":"https://paragraph.com/@charlemagnefang/digital-post-identity-in-the-open-marketplace-of-ideas","title":"Digital Post-Identity in the Open Marketplace of Ideas"},
    {"url":"https://paragraph.com/@charlemagnefang/dynasty-mindset","title":"Dynasty Mindset"},
    {"url":"https://paragraph.com/@charlemagnefang/four-notes-on-reading-remilia-collective-gp","title":"Four Notes on Reading Remilia Collective [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/gold-and-glory-in-times-of-thought-chaos","title":"Gold and Glory in Times of Thought-Chaos"},
    {"url":"https://paragraph.com/@charlemagnefang/kali-acc-basilisk-a-survival-horror-eschatology","title":"KALI/ACC Basilisk: A Survival Horror Eschatology"},
    {"url":"https://paragraph.com/@charlemagnefang/milady-as-a-total-art-gp","title":"Milady as a Total Art [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/milady-maker-notes-on-the-design-process","title":"Milady Maker: Notes on the Design Process"},
    {"url":"https://paragraph.com/@charlemagnefang/my-lightweight-travel-guide","title":"My lightweight travel guide"},
    {"url":"https://paragraph.com/@charlemagnefang/network-spirituality-collected-commentaries","title":"Network Spirituality, Collected Commentaries"},
    {"url":"https://paragraph.com/@charlemagnefang/nft-s-and-free-information","title":"NFT's and Free Information"},
    {"url":"https://paragraph.com/@charlemagnefang/notes-on-network-angels-and-god-guest-post-proanatwink","title":"Notes on Network Angels and God [Guest post: @proanatwink]"},
    {"url":"https://paragraph.com/@charlemagnefang/notes-on-the-new-net-art-and-network-spirituality-guest-post-eschatalogies","title":"Notes on the New Net Art and Network Spirituality [Guest post: @eschatalogies]"},
    {"url":"https://paragraph.com/@charlemagnefang/notes-on-the-new-wave-of-net-art","title":"Notes on the New Wave of Net Art"},
    {"url":"https://paragraph.com/@charlemagnefang/notes-on-the-vpl","title":"Notes on the VPL"},
    {"url":"https://paragraph.com/@charlemagnefang/notes-towards-a-study-of-remilia-s-art","title":"Notes towards a Study of Remilia's Art"},
    {"url":"https://paragraph.com/@charlemagnefang/nouns-wtf-a-self-seeding-dao-in-the-package-of-a-generative-pfpnft","title":"Nouns.wtf: A Self-Seeding DAO in the package of a Generative pfpNFT"},
    {"url":"https://paragraph.com/@charlemagnefang/on-jade-posting-gp","title":"On Jade Posting [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/on-secondary-a-suppressed-royalty-free-art-blocks-decentralization","title":"On Secondary: A Suppressed Royalty-free Art Blocks Decentralization"},
    {"url":"https://paragraph.com/@charlemagnefang/pfpnft-s-we-haven-t-seen-profile-first-design-yet","title":"pfpNFT's: We haven't seen Profile-first design yet"},
    {"url":"https://paragraph.com/@charlemagnefang/reality-after-the-wired","title":"Reality after the Wired"},
    {"url":"https://paragraph.com/@charlemagnefang/redacted-remilio-babies-notes-on-the-design-process","title":"Redacted Remilio Babies: Notes on the Design Process"},
    {"url":"https://paragraph.com/@charlemagnefang/remilia-corporation-external-memo-7-12-22-where-are-the-art-critics","title":"Remilia Corporation External Memo 7/12/22: Where are the Art Critics?"},
    {"url":"https://paragraph.com/@charlemagnefang/remilia-corporation-onboarding-package","title":"Remilia Corporation Onboarding Package"},
    {"url":"https://paragraph.com/@charlemagnefang/secondary-royalties-in-nft-inefficient-anti-market-ethically-suspect","title":"Secondary Royalties in NFT: Inefficient, anti-market & ethically suspect"},
    {"url":"https://paragraph.com/@charlemagnefang/the-cancelled-will-inherit-the-earth","title":"The Cancelled Will Inherit the Earth"},
    {"url":"https://paragraph.com/@charlemagnefang/the-new-lower-bound-of-network-spirituality-remilia-s-new-internet-as-reference-implementation-for-a-bottom-up-patchwork-gp","title":"The New Lower Bound of Network Spirituality: Remilia’s New Internet as Reference Implementation for a Bottom-Up Patchwork [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/the-nft-clearpill-solving-the-deed","title":"The NFT Clearpill: Solving the Deed"},
    {"url":"https://paragraph.com/@charlemagnefang/things-desired-an-egoless-online-gp","title":"Things Desired: An Egoless Online [gp]"},
    {"url":"https://paragraph.com/@charlemagnefang/unpacking-post-authorship","title":"Unpacking Post-Authorship"},
    {"url":"https://paragraph.com/@charlemagnefang/warholian-groupchat-2","title":"Warholian Groupchat"},
    {"url":"https://paragraph.com/@charlemagnefang/what-is-a-chibi-guest-post-ongestalte","title":"What is a chibi? [Guest post: @ongestalte]"},
    {"url":"https://paragraph.com/@charlemagnefang/what-remilia-believes-in-a-new-net-art-manifesto","title":"What Remilia Believes In: A New Net Art Manifesto"},
]

LEGACY_FILE_BY_URL = {
    "https://paragraph.com/@charlemagnefang/dynasty-mindset": "dynasty-mindset.md",
    "https://paragraph.com/@charlemagnefang/kali-acc-basilisk-a-survival-horror-eschatology": "kali-acc-basilisk.md",
    "https://paragraph.com/@charlemagnefang/what-remilia-believes-in-a-new-net-art-manifesto": "what-remilia-believes-in.md",
    "https://paragraph.com/@charlemagnefang/gold-and-glory-in-times-of-thought-chaos": "gold-and-glory.md",
    "https://paragraph.com/@charlemagnefang/alignment-fraud-cthulhu-hears-no-protest": "alignment-fraud.md",
    "https://paragraph.com/@charlemagnefang/the-cancelled-will-inherit-the-earth": "cancelled-will-inherit.md",
    "https://paragraph.com/@charlemagnefang/bonkler-critical-notes": "bonkler-critical-notes.md",
    "https://paragraph.com/@charlemagnefang/a-profile-on-milady-maker-s-charlotte-fang-gp": "milady-profile.md",
    "https://paragraph.com/@charlemagnefang/remilia-corporation-external-memo-7-12-22-where-are-the-art-critics": "external-memo-art-critics.md",
    "https://paragraph.com/@charlemagnefang/four-notes-on-reading-remilia-collective-gp": "four-notes-remilia.md",
    "https://paragraph.com/@charlemagnefang/redacted-remilio-babies-notes-on-the-design-process": "redacted-remilio-babies.md",
    "https://paragraph.com/@charlemagnefang/reality-after-the-wired": "reality-after-wired.md",
    "https://paragraph.com/@charlemagnefang/my-lightweight-travel-guide": "travel-guide.md",
    "https://paragraph.com/@charlemagnefang/on-jade-posting-gp": "jade-posting.md",
}


def read_key():
    if os.environ.get("FIRECRAWL_API_KEY"):
        return os.environ["FIRECRAWL_API_KEY"].strip()
    env_path = Path.home()/'.hermes'/'.env'
    for line in env_path.read_text(errors='ignore').splitlines():
        line=line.strip()
        if line.startswith('export FIRECRAWL_API_KEY=') or line.startswith('FIRECRAWL_API_KEY='):
            return line.split('=',1)[1].strip().strip('"').strip("'")
    raise RuntimeError('FIRECRAWL_API_KEY not found')


def slug_from_url(url):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", url.rstrip('/').split('/')[-1]).strip('-').lower()


def clean(md):
    md = md.replace('\r\n','\n')
    md = re.sub(r"\nChecking your Browser.*$", "", md, flags=re.S|re.I)
    md = re.sub(r"\nWallet · Privy.*$", "", md, flags=re.S)
    md = re.sub(r"\nStart writing\n\n20\d{2} .*$", "", md, flags=re.S)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    return md.strip()+"\n"


def scrape(api_key, url):
    payload={"url":url,"formats":["markdown"],"onlyMainContent":True,"maxAge":0}
    req=urllib.request.Request(API_URL, data=json.dumps(payload).encode(), headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"}, method='POST')
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def frontmatter(title, url, scraped_at):
    return "---\n" + f"title: {json.dumps(title, ensure_ascii=False)}\nsource: \"Golden Light / Paragraph\"\nurl: \"{url}\"\nscraped_at: \"{scraped_at}\"\n---\n\n"


def main():
    api_key=read_key()
    scraped_at=datetime.now(timezone.utc).isoformat()
    metadata=[]
    failures=[]
    for i, post in enumerate(POSTS,1):
        url=post['url']; title=post['title']; slug=slug_from_url(url)
        if url in LEGACY_FILE_BY_URL and (ROOT/LEGACY_FILE_BY_URL[url]).exists():
            path=LEGACY_FILE_BY_URL[url]
            chars=len((ROOT/path).read_text(errors='ignore'))
            print(f"[{i:02d}/{len(POSTS)}] exists {path}")
        else:
            path=f"{slug}.md"
            print(f"[{i:02d}/{len(POSTS)}] scrape {slug}")
            try:
                data=scrape(api_key,url)
                if not data.get('success'):
                    raise RuntimeError(json.dumps(data)[:500])
                md=clean((data.get('data') or {}).get('markdown') or '')
                if len(md)<300:
                    raise RuntimeError(f"suspiciously short markdown: {len(md)}")
                (ROOT/path).write_text(frontmatter(title,url,scraped_at)+md, encoding='utf-8')
                chars=len(md)
                time.sleep(0.75)
            except Exception as e:
                failures.append({"url":url,"title":title,"error":str(e)})
                print(f"  failed {e}")
                continue
        metadata.append({"title":title,"url":url,"path":path,"chars":chars,"source":"Golden Light / Paragraph"})
    (ROOT/'golden-light-metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')
    if failures:
        (ROOT/'golden-light-failures.json').write_text(json.dumps(failures, indent=2, ensure_ascii=False)+"\n", encoding='utf-8')
    else:
        p=ROOT/'golden-light-failures.json'
        if p.exists(): p.unlink()
    print(f"\nGolden Light discovered posts: {len(POSTS)}")
    print(f"Archived metadata entries: {len(metadata)}")
    print(f"Failures: {len(failures)}")
    return 0 if not failures else 2

if __name__=='__main__':
    raise SystemExit(main())
