import requests
import json
import logging
import time
from tqdm import tqdm

logging.basicConfig(filename='/Users/jose/Documents/program_projects/crm-migration/api-records.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

url = "https://api.hubapi.com/engagements/v1/engagements"

querystring = {"hapikey":""}

headers = {
    'Content-Type': "application/json",
}

# f = open('/Users/jose/Documents/program_projects/crm-migration/data/PAYLOAD.json')
f = open('/Users/jose/Documents/program_projects/crm-migration/data/failed.json')
data = json.load(f)

print('Data Loaded\n\nRunning...')

for i in tqdm(range(0, len(data))):
    if (i + 2) % 149 == 0:
        time.sleep(10)
    response = requests.request("POST", url, data=json.dumps(data[i]), headers=headers, params=querystring)
    if  response.status_code != 200:
        logging.error(f'{i} {response.status_code} {response.text}')
