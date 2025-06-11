import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API-TOKEN")

base_url = "https://api-ww.cert.orangecyberdefense.com"
headers = {"Authorization": TOKEN}
tag = "unc3886"
params = {"tags": tag}

response = requests.get(f"{base_url}/api/advisory/", headers=headers, params=params)
advisories = response.json()

if advisories['count'] == 0:
    print(f"No advisories found with tag '{tag}'")
    exit()

latest_advisory = advisories['items'][0]

response = requests.get(f"{base_url}/api/advisory/{latest_advisory['id']}", headers=headers)
advisory = response.json()
first_content_block = advisory['content_blocks'][-1]

print(f"{advisory['title']}\n\n{'-'.join(advisory['tags'])}\n\n\n{first_content_block['executive_summary']}\n\n")