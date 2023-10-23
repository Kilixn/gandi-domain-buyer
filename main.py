# automatically buys domain when expired via gandi.net api

import requests
import json
import time

from parameters import gandi_token, gandi_name, gandi_familyname, gandi_domain, dry_run, email_address, email_password
from email_func import send_email


url = "https://api.gandi.net/v5/domain/check"
querystring = {"name":gandi_domain}
headers = {'authorization': 'Bearer ' + gandi_token}

print(headers)
print(url)
response = requests.request("GET", url, headers=headers, params=querystring)

response_data = response.json()
availbility = response_data["products"][0]["status"]

while True:
    if availbility == "unavailable":
        print("domain is unavailable. retrying in 1 second")
        time.sleep(1)
    
    elif availbility == "available":
        print("domain is available. buying domain now...")
    
        url = "https://api.gandi.net/v5/domain/domains"

        # NOTE: dry-run is for testing. if you wanto to buy the domain remove dry-run argument
        payload = "{\"fqdn\":\"" + gandi_domain + "\",\"duration\":5,\"owner\":{\"city\":\"Paris\",\"given\":\"" + gandi_name + "\",\"family\":\"" + gandi_familyname + "\",\"zip\":\"75001\",\"country\":\"FR\",\"streetaddr\":\"5 rue neuve\",\"phone\":\"+33.123456789\",\"state\":\"FR-IDF\",\"type\":\"individual\",\"email\":\"alice@example.org\"}}"
        if dry_run is True:
            headers = {
                'authorization': 'Bearer ' + gandi_token,
                'content-type': "application/json",
                'dry-run': "1"
                }
        else:
            headers = {
                'authorization': 'Bearer ' + gandi_token,
                'content-type': "application/json"
                }

        response = requests.request("POST", url, data=payload, headers=headers)
        response = response.json()
    
        print(response["status"])
        if response["status"] == "success":
            send_email(f"automatically bought new domain via gandi.net", f"domain is {gandi_domain}. NOTE: also quitting program.")
            quit()