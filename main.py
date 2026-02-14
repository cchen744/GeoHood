'''
Purpose: Convert address to zipcode, then use it to extract housing information
'''
import json
import argparse
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import geopy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import more if you need more packages

API_KEY = 'AIzaSyBuNHyspdHBMXTf4usN-WXnZ3RxcK_RarU' # input your geocoding api key

class WebScraper():
    def __init__(self):
        pass

    # Input the address
    def geocoding(self, address):
        params = {
            "address": address,
            "key": API_KEY
        }
        # Send a request to Google geocoding
        response = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json", params=params)
        # Parse and validate the response
        data = response.json()
        status = data.get('status')
        if status != 'OK':
            error = data.get('error_message', '<no message>')
            # provide a clear exception so callers can act accordingly
            raise RuntimeError(f"Geocoding request failed ({status}): {error}")
        # Extract zipcode and coordinate from json file
        zipcode = data['results'][0]['address_components'][-1]['long_name']
        coordinate = data['results'][0]['geometry']['location']
        return zipcode, coordinate

        # Input the zipcode of the target region

    def get_houses(self, zipcode):
        # Use Selenium to render JavaScript and get dynamically loaded listings
        print(f"[INFO] Opening Redfin page for zipcode {zipcode}...")
        
        driver = webdriver.Chrome()
        try:
            url = f"https://www.redfin.com/zipcode/{zipcode}"
            driver.get(url)
            
            # Wait for house listings to load (max 10 seconds)
            # Look for a listing element or container - adjust the selector as needed
            print("[INFO] Waiting for listings to load...")
            wait = WebDriverWait(driver, 10)
            # Try to wait for a common listing container to appear
            try:
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='home-card']")))
            except:
                print("[WARNING] Timeout waiting for listings - page may have loaded anyway")
            
            # Get the rendered HTML
            rendered_html = driver.page_source
            soup = BeautifulSoup(rendered_html, 'html.parser')
            
            self.house_collection = []
            
            # Find all home cards (adjust selector if Redfin uses different classes)
            listing_containers = soup.find_all('div', {'data-testid': 'home-card'})
            print(f"[INFO] Found {len(listing_containers)} listings")
            
            if len(listing_containers) == 0:
                print("[WARNING] No listings found with home-card selector, trying alternative...")
                # Fallback: try to find any listing divs
                listing_containers = soup.find_all('div', class_=['home-card', 'listing-card', 'PropertyCard'])
            
            for i, listing in enumerate(listing_containers):
                try:
                    # Extract price
                    price_elem = listing.find(string=lambda text: text and '$' in str(text))
                    if not price_elem:
                        continue
                    price = price_elem.strip()
                    
                    # Extract address
                    address_elem = listing.find('a', {'data-testid': 'property-address'})
                    if not address_elem:
                        address_elem = listing.find('a', class_='address')
                    if not address_elem:
                        continue
                    house_address = address_elem.text.strip()
                    
                    # Extract coordinates (might be in data attributes or text)
                    coord_text = listing.get('data-lat') or listing.get('data-lng')
                    if coord_text:
                        coordinate = {"lat": float(listing.get('data-lat', 0)), "lng": float(listing.get('data-lng', 0))}
                    else:
                        # Default to Madison if not found
                        coordinate = {"lat": 43.07, "lng": -89.40}
                    
                    # Extract image URL
                    img_elem = listing.find('img', class_=['home-image', 'listing-image'])
                    if not img_elem:
                        img_elem = listing.find('img')
                    image_url = img_elem.get('src') if img_elem else ""
                    if not image_url:
                        continue
                    
                    house = House(price, house_address, coordinate, image_url)
                    self.house_collection.append(house)
                    print(f"[SUCCESS] Listed house {i+1}: {price} @ {house_address}")
                    
                except (AttributeError, TypeError, KeyError, ValueError) as e:
                    print(f"[SKIP] Could not parse listing {i}: {e}")
                    continue
        
        finally:
            driver.quit()
            print("[INFO] Browser closed")


    # Save house information to csv and photos to a folder
    def save_houses(self, zipcode):
        path = f"houses_{zipcode}"  # Create a folder to save house photos
        df = pd.DataFrame([house.get_info() for house in self.house_collection])
        df.to_csv(f"properties_{zipcode}.csv", index=False)
        for house in self.house_collection:  # Iterate all houses in the house collection
            house.save_file()  # Save house information as file
            house.save_img(path)  # Save house image to the path
        


class House():
    def __init__(self, price, house_address, coordinate, image_url): # information we want to get
        # Set house attributes
        self.price = price
        self.house_address = house_address
        self.coordinate = coordinate
        self.image_url = image_url

    def get_info(self):
        house_info = {
            "price": self.price,
            "address": self.house_address,
            "coordinate": self.coordinate,
            "image_url": self.image_url
        }
        return house_info

    def save_img(self, path):  # Save house images to the path
        img = requests.get(self.image_url).content
        with open(f"{path}/{self.house_address}.jpg", 'wb') as f:
            f.write(img)

    def save_file(self):
        """Persist this house's info as a small JSON file in the current directory.

        The name is derived from the house address so multiple entries don't
        collide (slashes are replaced with underscores).
        """
        safe_name = self.house_address.replace('/', '_').replace(' ', '_')
        filename = f"{safe_name}.json"
        with open(filename, 'w') as f:
            json.dump(self.get_info(), f, indent=2)


if __name__ == '__main__':
    # Add arguments for command line execution
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', type=str, required=True, help='Please input the address you want to look for')
    args = parser.parse_args()

    web_scraper = WebScraper()  # Create a webscraper instance
    zipcode, coordinate = web_scraper.geocoding(args.address)  # Send the address to the webscraper to get the zipcode
    web_scraper.get_houses(zipcode)  # Collect a set of houses and their information based on zip code
    web_scraper.save_houses(zipcode)  # Save house information into files

# we got some issues at this stage:
# 1. The geocoding function is working well, but the final output csv is empty.
# 2. The intended picture path is not created, and no images are saved.