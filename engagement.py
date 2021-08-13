import requests
import json
import logging
import time
from tqdm import tqdm

logging.basicConfig(filename='/Users/jose/Documents/program_projects/crm-migration/api-records.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

url = "https://api.hubapi.com/engagements/v1/engagements"

querystring = {"hapikey":"97c5dee7-a000-4588-84fd-e3b6f4b44c24"}

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

# payload = json.dumps({
#     "engagement": {
#         "active": 'true',
#         "ownerId": 1,
#         "type": "NOTE",
#         "timestamp": 1409172644778
#     },
#     "associations": {
#         "contactIds": [11877974],
#         "companyIds": [ ],
#         "dealIds": [ ],
#         "ownerIds": [ ]
#     },
#     "attachments": [
#         {
#             "id": 4241968539
#         }
#     ],
#     "metadata": {
#         "body": "note body"
#     }
# })

# headers = {
#     'Content-Type': "application/json",
#     }

# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

# print(response.text)