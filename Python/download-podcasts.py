import sys
import feedparser
import requests

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <feed_url> <list||download> <number>")
        sys.exit(1)

    rss_feed = sys.argv[1]
    option = sys.argv[2]
    number = int(sys.argv[3])

    if option not in ["list", "download"]:
        print("Usage: python script.py <feed_url> <list||download> <number>")
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
        filename = f"{entry.title}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")

if __name__ == "__main__":
    main()
