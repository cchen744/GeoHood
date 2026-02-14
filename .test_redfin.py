import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
resp = requests.get("https://www.redfin.com/zipcode/53705", headers=headers)
soup = BeautifulSoup(resp.content, 'html.parser')

# Save for inspection
with open("sample_redfin.html", "w") as f:
    f.write(soup.prettify()[:10000])  # First 10k chars

# Try to find what divs/classes actually exist
print("=== Looking for common patterns ===\n")

# Find all divs and their classes
divs = soup.find_all('div', limit=50)
for div in divs:
    classes = div.get('class', [])
    if classes:
        print(f"Classes: {classes}")

print("\n=== Looking for prices (currency patterns) ===")
price_patterns = soup.find_all(string=lambda text: text and '$' in str(text))
for p in price_patterns[:5]:
    print(p)

print("\n=== HTML structure sample ===")
print(soup.prettify()[:3000])
