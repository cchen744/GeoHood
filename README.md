# Real-Estate Data Collection Pipeline

An object-oriented Python pipeline for collecting residential real-estate listings
from the web and turning them into clean, analysis-ready data. It combines HTTP
requests, HTML/JSON-LD parsing, geocoding, and photo retrieval into a single
reusable tool.

## What it does

- Fetches listing pages with `requests` using realistic browser headers
- Parses each listing card with `BeautifulSoup`, pulling **price** from the card
  and **address** from embedded `JSON-LD` `PostalAddress` records
- Geocodes addresses to coordinates via the Google Geocoding API
- Retrieves nearby geotagged photos via the Flickr API
- Exports a clean CSV of `house_id, price, address`
- Ships with an offline HTML snapshot so results are fully reproducible without
  hitting a live site

## Quick start

```bash
pip install -r requirements.txt

# Parse the bundled offline sample (no network needed)
python scraper.py --offline sample_data --out houses.csv
```

Live scraping (subject to the target site's rate limiting / anti-bot measures):

```bash
python scraper.py --zip 53703 --out houses.csv
```

## Design

The scraper is split into small, testable classes:

- `ListingPageParser` — turns one page of HTML into `(price, address)` rows,
  matching listing cards to JSON-LD addresses by listing id
- `RealEstateScraper` — orchestrates fetching (live ZIP or offline pack) and CSV export

`real_estate_scraper.ipynb` is the exploratory notebook covering the full workflow:
`requests` basics, POST requests, the Flickr API, Google geocoding, and
`BeautifulSoup` parsing.

## Files

| Path | Purpose |
|------|---------|
| `scraper.py` | Standalone CLI scraper (OOP) |
| `real_estate_scraper.ipynb` | Exploratory notebook of the full pipeline |
| `sample_data/` | Offline HTML snapshot + `meta.csv` for reproducible parsing |

## Notes

API keys in the notebook are placeholders (`YOUR_GOOGLE_API_KEY`,
`YOUR_FLICKR_API_KEY`). Supply your own to run the geocoding and photo cells.

## Tech

Python · requests · BeautifulSoup · pandas · argparse
