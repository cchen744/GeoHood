"""
Real-estate listing scraper.

Given a ZIP code (or a local offline HTML snapshot), collects each listing's
price and address into a clean CSV. Written with an object-oriented design so
the fetching, parsing, and export stages are independently testable.

Usage
-----
    # Parse the bundled offline sample (no network needed)
    python scraper.py --offline sample_data --out houses.csv

    # Scrape a live ZIP code (may be rate-limited / blocked by the site)
    python scraper.py --zip 53703 --out houses.csv
"""

import argparse
import json
import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _find_postal_addresses(obj):
    """Recursively collect every JSON-LD PostalAddress dict in a nested object."""
    found = []
    if isinstance(obj, dict):
        if obj.get("@type") == "PostalAddress":
            found.append(obj)
        for value in obj.values():
            found.extend(_find_postal_addresses(value))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_find_postal_addresses(item))
    return found


class ListingPageParser:
    """Extracts (price, address) rows from one listing page's HTML."""

    def parse(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        cards = soup.find_all("div", class_=re.compile(r"HomeCardContainer"))

        # Build a listing-id -> address map from JSON-LD blocks.
        id_to_address = {}
        for script in soup.find_all("script", {"type": "application/ld+json"}):
            if not script.string:
                continue
            try:
                data = json.loads(script.string)
            except json.JSONDecodeError:
                continue
            objects = data.get("@graph", data) if isinstance(data, dict) else data
            objects = objects if isinstance(objects, list) else [objects]
            for obj in objects:
                if isinstance(obj, dict) and obj.get("identifier"):
                    addrs = _find_postal_addresses(obj)
                    if addrs:
                        id_to_address[obj["identifier"]] = addrs[0]

        rows = []
        for card in cards:
            listing_id = card.attrs.get("data-listing-id")
            if not listing_id or listing_id not in id_to_address:
                continue
            price_span = card.find("span", class_=re.compile(r"Price"))
            price = price_span.text.strip() if price_span else None
            a = id_to_address[listing_id]
            parts = [
                a.get("streetAddress", ""),
                a.get("addressLocality", ""),
                a.get("addressRegion", ""),
                a.get("postalCode", ""),
            ]
            address = ", ".join(p for p in parts if p)
            rows.append({"house_id": listing_id, "price": price, "address": address})
        return rows


class RealEstateScraper:
    """Fetches listing pages (live or offline) and exports a clean CSV."""

    def __init__(self, parser=None):
        self.parser = parser or ListingPageParser()

    def from_live_zip(self, zip_code):
        url = f"https://www.redfin.com/zipcode/{zip_code}"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return self.parser.parse(resp.text)

    def from_offline_pack(self, root):
        meta = pd.read_csv(os.path.join(root, "meta.csv"))
        html_dir = os.path.join(root, "raw_html")
        rows = []
        for _, r in meta.iterrows():
            with open(os.path.join(html_dir, r["filename"]), encoding="utf-8") as f:
                rows.extend(self.parser.parse(f.read()))
        return rows

    @staticmethod
    def export(rows, out_path):
        df = pd.DataFrame(rows)
        df.to_csv(out_path, index=False)
        return df


def main():
    ap = argparse.ArgumentParser(description="Collect real-estate listings to CSV.")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--zip", help="ZIP code to scrape live")
    group.add_argument("--offline", help="Path to an offline HTML pack folder")
    ap.add_argument("--out", default="houses.csv", help="Output CSV path")
    args = ap.parse_args()

    scraper = RealEstateScraper()
    rows = (
        scraper.from_live_zip(args.zip)
        if args.zip
        else scraper.from_offline_pack(args.offline)
    )
    df = scraper.export(rows, args.out)
    print(f"Saved {len(df)} listings to {args.out}")
    print(df.head())


if __name__ == "__main__":
    main()
