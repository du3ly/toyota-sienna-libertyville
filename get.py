"""
This script will scrape inventory (Sienna AWD) from Toyota Libertyville
"""

import requests
import json
from bs4 import BeautifulSoup

search_libertyville_url = "https://www.autonationtoyotalibertyville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?model=Sienna&normalDriveLine=AWD"

def get_data(url):
    r = requests.get(url)
    if(r.status_code == 200):
        return r.json()
    else:
        print(r.status_code)

def pretty_print(response):
    print(json.dumps(response, indent=4))

def parse_data(data):
    print('status - inventory date - VIN - msrp - interior color - exterior color - trim') 
    count = 1
    resp = data['pageInfo']
    #totalCount = resp['totalCount']
    
    for key in resp['trackingData']:
        print("{0}. {1} - {2} - {3} - {4} - {5} - {6} - {7}".format(count, key['status'], key['inventoryDate'] ,key['vin'], key['msrp'], key['interiorColor'], key['exteriorColor'], key['trim']))
        count += 1
    

if __name__ == "__main__":
    response = get_data(search_libertyville_url)
    #pretty_print(response)
    parse_data(response)
