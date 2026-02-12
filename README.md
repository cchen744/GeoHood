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
│
├── properties.csv          # All property listings with prices, addresses, photo paths
├── coordinates.csv         # Geographic coordinates for each property
└── property_photos/        # Folder containing downloaded property images
    ├── 123_main_st.jpg
    ├── 456_oak_ave.jpg
    └── ...
    
### Output Format
properties.csv
Price	Address	ZIP	Photo_Path
$450,000	123 Main St	53705	property_photos/123_main_st.jpg
coordinates.csv
Address	Latitude	Longitude
123 Main St	43.0731	-89.4012

### Example
python main.py --address="4849 Sheboygan Ave, Madison, WI"

This will:

Geocode "4849 Sheboygan Ave, Madison, WI" to find ZIP code 53705

Scrape all Redfin listings in 53705

Generate CSV files with property details and coordinates

Download property photos to the property_photos folder
