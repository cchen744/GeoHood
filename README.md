# GeoHood
A Python web scraper that collects housing data from Redfin for a given address. The tool automatically identifies the ZIP code of the input address and scrapes detailed information about all properties in that area.

Features
Address-based discovery – Input any address, automatically find its ZIP code, and scrape all houses in that postal area

Comprehensive property data – Collects for each property:

House price

Full address

Geographic coordinates (saved as CSV)

At least one property photo

Object-Oriented Design – Clean, maintainable code following OOP principles

Single file implementation – Easy to run and grade

## Quick Start
### Prerequisites
Python 3.7+

Required packages: requests, beautifulsoup4, pandas, geopy, argparse

### Installation
pip install requests beautifulsoup4 pandas geopy

### Usage
Run the scraper with a single command:

python geohood.py --address="4849 Sheboygan Ave, Madison, WI"

## Output Structure
When you run the script, it creates:

output/
<br>│
<br>├── f"properties_{zipcode}.csv"          # All property listings with prices, addresses, photo paths
<br>└── f"houses_{zipcode}"/        # Folder containing downloaded property images
    <br>├── 123_main_st.jpg
    <br>├── 456_oak_ave.jpg
    <br>└── ...
    
### Output Format
properties_{zipcode}.csv (single file containing all fields)
Price	Address	ZIP	Latitude	Longitude	Photo_Path
$450,000	123 Main St	53705	43.0731	-89.4012	houses_{zipcode}/123_main_st.jpg

> **Note:** coordinates are included as columns in the same CSV.

### Example
python main.py --address="4849 Sheboygan Ave, Madison, WI"

This will:

Geocode "4849 Sheboygan Ave, Madison, WI" to find ZIP code 53705

Scrape all Redfin listings in 53705

Generate CSV files with property details and coordinates

Download property photos to the property_photos folder

### Temporary
Submit the code (.py) and CSV files with house information.
Checkpoint date: you need to finish 75% of functions.

Task 1:
- Prof. Robert Roth plans to create a map to visualize the houses nearby a specific place. He hopes you can help him to create a web scraper for Redfin house information collection (follow the OOP paradigm). The input might be an address. He expects to have a csv file which contains information for all the houses located in the same zip code. For each house, house price, address, coordinates (a CSV file), and at least one photo should be collected and saved.
