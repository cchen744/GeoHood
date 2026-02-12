'''
Purpose: Convert address to zipcode, then use it to extract housing information

'''

import json
import argparse
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
# import more if you need more packages

API_KEY = '...' # input your geocoding api key

class WebScraper():
    def __init__(self):
        pass

    # Input the address
    def geocoding(address):
        params = {
            "address": address,
            "key": API_KEY
        }
        # Send a request to Google geocoding
        response = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json", params=params)
        # Get the coordinates from the response
        data = response.text
        # Extract zipcode and coordinate from json file
        ...
        return zipcode, coordinate

        # Input the zipcode of the target region

    def get_houses(self, zipcode):
        # Send a request to the REDFIN to get house information
        headers = {
            # Add headers in case the system identify you as a robot
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        response = requests.get(url=f"https://www.redfin.com/zipcode/{zipcode}", headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        self.house_collection = []
        all_houses = soup.find_all()

        for house in all_houses:
            house = House()
            house.get_info()  # Get house information
            all_houses.append(house)
        ...


    # Save house information to csv and photos to a folder
    def save_houses(self, zipcode):
        ...
        for house in self.house_collection():  # Iterate all houses in the house collection
            house.save_file()  # Save house information as file
            house.save_img(path)  # Save house photos to the path
        ...


class House():
    def __init__(self, price, house_address, coordinate, image_url): # information we want to get
        # Set house attributes
        self.price = price
        ...

    def get_info(self):
        house_info =  # Collect a set of attributes of houses
        return house_info

    def save_img(self, path):  # Save house images to the path
        img = requests.get(self.image_url).content
        ...



# Add arguments for command line execution
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=str, required=True, help='Please input the address you want to look for')

web_scraper = WebScraper()  # Create a webscraper instance
web_scraper.geocoding(args.address)  # Send the address to the webscraper to get the zipcode
print('Zipcode: {} || Step1 GetZipcode succeeded!\n'.format(zipcode))
web_scraper.get_houses(zipcode)  # Collect a set of houses and their information based on zip code
web_scraper.save_houses()  # Save house information into files