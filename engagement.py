import requests
import json

url = "https://api.hubapi.com/engagements/v1/engagements"

querystring = {"hapikey":"97c5dee7-a000-4588-84fd-e3b6f4b44c24"}

headers = {
    'Content-Type': "application/json",
}

f = open('/Users/jose/Documents/program_projects/crm-migration/JSON-exports/PAYLOAD_TEST.json')
data = json.load(f)

for item in data:
    response = requests.request("POST", url, data=json.dumps(item), headers=headers, params=querystring)
    print(response.status_code)

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