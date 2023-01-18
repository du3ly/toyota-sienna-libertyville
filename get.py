"""
This script will scrape inventory (Sienna AWD) from Toyota Libertyville and outputs the results to Discord
"""

import requests
import json
from discord_webhook import DiscordWebhook

search_libertyville_url = "https://www.autonationtoyotalibertyville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?model=Sienna&normalDriveLine=AWD"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1065366415630147714/-5EfNgobI9Pize0xAcKiqyjjF9vJR51cXDzHS7HZMknFrYgvAuBqY67coxRrjdoyt6UR"

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
    heading = "status - inventory date - VIN - msrp - interior color - exterior color - trim"
    count = 1
    resp = data['pageInfo']

    send_headings = title + "\n" + heading + "\n"
    discord_webhook(send_headings)

    for key in resp['trackingData']:
        #print("{0}. {1} - {2} - {3} - {4} - {5} - {6} - {7}".format(count, key['status'], key['inventoryDate'] ,key['vin'], key['msrp'], key['interiorColor'], key['exteriorColor'], key['trim']))
        inventory_data = ("{0}. {1} - {2} - {3} - {4} - {5} - {6} - {7}".format(count, key['status'], key['inventoryDate'] ,key['vin'], key['msrp'], key['interiorColor'], key['exteriorColor'], key['trim']))
        discord_webhook(inventory_data)
        count += 1


def discord_webhook(data):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=data)
    response = webhook.execute()

if __name__ == "__main__":
    response = get_data(search_libertyville_url)
    #pretty_print(response)
    parse_data = parse_data(response)
