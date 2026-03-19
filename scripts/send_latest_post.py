import requests
import xml.etree.ElementTree as ET
import os
import json

RSS_URL = "https://rhysearching.com/feed.xml"
LAMBDA_ENDPOINT = os.environ.get("NEWSLETTER_ENDPOINT")


def get_latest_post():
    response = requests.get(RSS_URL)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    channel = root.find("channel")
    if channel is None:
        raise Exception("RSS missing channel")

    items = channel.findall("item")

    for item in items:
        title = item.findtext("title")
        link = item.findtext("link")
        pub_date = item.findtext("pubDate")

        # Skip disclaimer
        if "disclaimer" in (link or "").lower():
            continue

        return {
            "title": title,
            "link": link,
            "pub_date": pub_date
        }

    raise Exception("No valid posts found")


def main():
    post = get_latest_post()

    payload = {
        "title": post["title"],
        "link": post["link"],
        "pub_date": post["pub_date"]
    }

    response = requests.post(
        LAMBDA_ENDPOINT,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        raise Exception("Failed to trigger newsletter")


if __name__ == "__main__":
    main()