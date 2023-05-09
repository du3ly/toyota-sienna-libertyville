"""
This script will scrape inventory (Sienna AWD) from Toyota Libertyville and outputs the results to Discord
"""

import requests
import json
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
load_dotenv()

search_libertyville_url = "https://www.autonationtoyotalibertyville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?model=Sienna&normalDriveLine=AWD"
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def get_data(url):
    r = requests.get(url)
    if(r.status_code == 200):
        return r.json()
    else:
        print(r.status_code)

def pretty_print(response):
    print(json.dumps(response, indent=4))

def parse_data(data):
    title = "Toyota Libertyville"
    heading = "status - inventory date - VIN - msrp - exterior color - interior color - trim"
    count = 1

    send_headings = title + "\n" + heading + "\n"

    new = []
    new_inventory = []
    file1 = open('vins.txt', 'a')

    current = read_vins()

    for key in data:
        if key['vin'] not in current:
          new.append(key['vin'])
          #print("{0}. {1} - {2} - {3} - {4} - {5} - {6} - {7}".format(count, key['status'], key['inventoryDate'] ,key['vin'], key['msrp'], key['exteriorColor'], key['interiorColor'], key['trim']))
          inventory_data = ("{0}. {1} - {2} - {3} - {4} - {5} - {6} - {7}".format(count, key['status'], key['inventoryDate'] ,key['vin'], key['msrp'], key['exteriorColor'], key['interiorColor'], key['trim']))
          new_inventory.append(inventory_data)
          count += 1

    for key in new:
      file1.write(key + '\n')

    # Send new inventory to Discord
    if new_inventory:
      discord_webhook(send_headings)
      for i in new_inventory:
        discord_webhook(i)

def get_inventory(data):
    inventory = []
    resp_json = data['pageInfo']
    resp_array = resp_json['trackingData']
    for resp in resp_array:
      car = {
        "status": resp['status'],
        "inventoryDate": resp['inventoryDate'],
        "vin": resp['vin'],
        "msrp": resp['msrp'],
        "exteriorColor": resp['exteriorColor'],
        "interiorColor": resp['interiorColor'],
        "trim": resp['trim']
      } 
      inventory.append(car)
    return inventory

def read_vins():
    file1 = open('vins.txt', 'r')
    data = file1.read().split('\n')
    file1.close()
    return data

def discord_webhook(data):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=data)
    response = webhook.execute()

if __name__ == "__main__":
    response = get_data(search_libertyville_url)
    inventory = get_inventory(response)
    parse_data(inventory)
