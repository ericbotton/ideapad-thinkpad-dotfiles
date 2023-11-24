#!/usr/bin/python3

import sys
import os
import feedparser
import requests
from pathlib import Path

RADIOLAB = 'https://feeds.feedburner.com/radiolab'

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <rss_feed> <list|download> <number>")
        sys.exit(1)

    rss_feed = sys.argv[1]
    option = sys.argv[2]
    number = int(sys.argv[3])

    if option not in ["list", "download"]:
        print("Invalid option. Choose either 'list' or 'download'.")
        sys.exit(1)

    feed = feedparser.parse(rss_feed)
    entries = feed.entries

    if option == "list":
        for i, entry in enumerate(entries[:number]):
            print(f"{i+1}. {entry.title}")
    elif option == "download":
        entry = entries[number-1]
        url = entry.links[0].href
        response = requests.get(url)
        
        podcast_filename = f"{entry.title}.mp3"

        print('entry.links[0].href == ', podcast_filename)
        # Replace invalid characters with underscore
        invalid_chars = " <>:\"\\|?*"
        for char in invalid_chars:
            podcast_filename = podcast_filename.replace(char, "_")
            
        filename = Path.home() / 'Downloads' / 'Podcasts' / podcast_filename
        print('podcast path = ', filename)

        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")

if __name__ == "__main__":
    main()

### PowerShell example:
### download list of 8 podcasts
# $podcast_array = "8", "7", "6", "5", "4", "3", "2", "1"
# foreach ($i in $podcast_array) {
# Write-Host "i==$i"
# py .\podcast-download.py 'https://feeds.feedburner.com/radiolab' download $i
# }
