import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os

TARGET_URL = "https://example.com/articles"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_CSV = os.path.join("data", "data.csv")
os.makedirs("data", exist_ok=True)

def fetch_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_list_page(html):
    soup = BeautifulSoup(html, "lxml")
    items = []

    for card in soup.select("article"):
        title_tag = card.select_one("h2 a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href")
        items.append({"title": title, "link": link, "scraped_at": datetime.utcnow().isoformat()})
    return items

def save_items(items):
    df = pd.DataFrame(items)
    df.to_csv(OUTPUT_CSV, index=False)
    print("Saved:", OUTPUT_CSV)

def main():
    html = fetch_page(TARGET_URL)
    items = parse_list_page(html)
    save_items(items)

if __name__ == "__main__":
    main()
