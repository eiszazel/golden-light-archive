---
title: "Why Torrent"
source: "Remilia Corporation Blog"
url: "https://blog.remilia.org/how-to-torrent"
scraped_at: "2026-05-07T15:59:56.050781+00:00"
original_map_title: "Why Torrent"
---

Sep 24, 2021

Foolproof guide on the easiest way to download free movies through a torrent search engine, qBittorrent. 5 minutes to setup!

# Why Torrent

123movies doesn't cut it. If you torrent you have a much more complete selection of movies/tv shows, higher quality, with the files saved on your end in case streaming sites go down.

# Step-by-Step Guide

## 1\. Download & Install qBittorrent:

[qBittorrent Official Website\\
\\
qBittorrent Official Website\\
\\
![](https://www.qbittorrent.org/favicon.ico)qBittorrent Development Team: https://github.com/qbittorrent\\
\\
![](https://www.qbittorrent.org/img/os/winlogo.png.pagespeed.ce.WH51vjrRPS.png)](https://www.qbittorrent.org/download.php?ref=blog.remilia.org)

## 2\. Enable Search Engine

Go to `View > Search Engine` and turn it on

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-5.png)

You'll see a new Search tab appear next to Transfers, above the `Status` sidebar:

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-6.png)

If you are on OSX (Mac), you might get the error `Your Python version (2.7.16) is outdated. Please upgrade to latest version for search engines to work`.

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/aOZTty7u.jpg)

No worries. Open the application "Terminal" (Finder: Applications > Terminal > Terminal.app), and type in and hit enter:

`ruby -e "$(curl -fsSL` [https://raw.githubusercontent.com/Homebrew/install/master/install](https://raw.githubusercontent.com/Homebrew/install/master/install?ref=blog.remilia.org))`"
`

Enter your computer password if prompted.

Let it run, it will take about 10 minutes on a fast connection.

When it finishes type in `brew install python3` and hit enter.

Now go back to qBittorent and try again.

## 3\. Setup the Search Engine

Navigate to the `Search` tab, and you'll see a message saying `There aren't any search plugins installed`. Before we can search torrents, we'll need to add in some sources for the client to look for.

Click the `Search plugins...` button at the bottom right.

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-7.png)

Click `Install a new one`

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-8.png)

A popup will appear. Click `Web link`

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-10.png)

Enter the following url to add 1337x.to and hit OK:

[`https://gist.githubusercontent.com/sa3dany/1478e311e6371a60e251e7bdfc2dda65/raw/6288d84627e23823427d03f7aca2f492aa0c8338/one337x.py`](https://gist.githubusercontent.com/sa3dany/1478e311e6371a60e251e7bdfc2dda65/raw/6288d84627e23823427d03f7aca2f492aa0c8338/one337x.py?ref=blog.remilia.org)

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-12.png)

Repeat the process to add Nyaa.pantsu:

[`https://raw.githubusercontent.com/libellula/qbt-plugins/main/pantsu.py`](https://raw.githubusercontent.com/libellula/qbt-plugins/main/pantsu.py?ref=blog.remilia.org)

And then again for YTS.am:

[`https://raw.githubusercontent.com/khensolomon/leyts/master/yts.py`](https://raw.githubusercontent.com/khensolomon/leyts/master/yts.py?ref=blog.remilia.org)

This will be a solid set of torrent sources. 1337x and YTS cover all mainstream films and television, and nyaa is comprehensive for anime. If you need additional sources, [a full list is here](https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins?ref=blog.remilia.org), the urls can be found by clicking the download button

## Torrent New Movies

Now simply enter any movie you're looking for into the search bar, and torrent results will come up.

Pick one at the right size (ideally no less than 2GB for 1080p; no less than 1GB for 720p) with a healthy number of seeders (ideally more than 10) as you normally would:

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-11.png)

All done, you'll find the torrents appear as normal in your Transfers section.

# Additional Info

## Recommended Streaming Client

[MPV](https://mpv.io/installation/?ref=blog.remilia.org)

## Where to Get Subs

[opensubtitles.org](https://blog.remilia.org/how-to-torrent/opensubtitles.org)

You can just drag and drop the subtitles onto the MPV video.

## Disable Seeding

Navigate to \`Tools > Options > Connection\` and change `Global maximum number of upload slots` and `Maximum number of upload slots per torrent` to 0:

![](https://storage.ghost.io/c/34/4d/344db379-6ee0-4527-979b-c712c2e2f368/content/images/2021/09/image-16.png)

## Setup VPN

Coming soon

* * *

Look forward to Torrenting for Boys: Automate high-speed downloading on USENET with Sonarr & Radarr onto Plex's self-hosted streaming service!

* * *

Tags: [Guide](https://blog.remilia.org/tag/guide/)

Permalink: _https://blog.remilia.org/how-to-torrent/_
