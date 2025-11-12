import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API-TOKEN")

base_url = "https://api-ww.cert.orangecyberdefense.com"
headers = {"Authorization": TOKEN}


# List Advisories (with limit)
print("########################################################################################")
print("### List Advisories with default sort (timestamp updated) and limited to the first 2 ###")
print("########################################################################################")

params = {"limit": 2}
response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()["items"]
print(f"{advisories[0]['id']} - '{advisories[0]['title']}'\n{advisories[1]['id']} - '{advisories[1]['title']}'")
print('\n')


# List Advisories (string in title)
print("######################################################################################################")
print("### List Advisories with default sort (timestamp updated) and limit (30) that have 'salt' in title ###")
print("######################################################################################################")

params = {"title": "salt"}
response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()
if advisories['count'] == 0:
    print("No advisories found that has 'salt' in title")
else:
    for item in advisories["items"]:
        print(f"{item['id']} - '{item['title']}'")
print('\n')


# List Advisories (severity above 3)
print("##################################################################################################")
print("### List Advisories with default sort (timestamp updated) and limit (5) that have severity > 4 ###")
print("##################################################################################################")

params = {"severity": "4,5", "limit": 5}
response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()
if advisories['count'] == 0:
    print("No advisories found that has severity 4 or 5")
else:
    for item in advisories["items"]:
        print(f"{item['id']} - '{item['title']}' - {item['severity']}")
print('\n')


# Get latest advisory's first executive summary
print("################################################################################################")
print("### Get the first content block from the latest advisory (first content block is the oldest) ###")
print("################################################################################################")

params = {}
response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()
latest_advisory = advisories['items'][0]
response = requests.get(f"{base_url}/api/advisory/{latest_advisory['id']}", headers=headers)
advisory = response.json()
first_content_block = advisory['content_blocks'][-1]
print(f"{advisory['title']}\n{'-'.join(advisory['tags'])}\n\n{first_content_block['executive_summary'][:100]}\n\n")


# Get latest advisory (that has category ecosystem) as HTML
print("##############################################################################")
print("### Get the latest advisory with category 'ecosystem' as preformatted HTML ###")
print("##############################################################################")

params = {"categories": "ecosystem", "limit": 1}
response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()
advisory = advisories['items'][0]
response = requests.get(f"{base_url}/api/advisory/{advisory['id']}/html", headers=headers)
advisory = response.json()
with open(f"advisory_{advisory['id']}.html", "w+") as f:
    f.write(advisory["html"])
print(f"Advisory {advisory['id']} was written to advisory_{advisory['id']}.html")
