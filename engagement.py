import requests
import json

url = "https://api.hubapi.com/engagements/v1/engagements"

querystring = {"hapikey":"Angle Tasks"}

payload = json.dumps({
    "engagement": {
        "active": 'true',
        "ownerId": 1,
        "type": "NOTE",
        "timestamp": 1409172644778
    },
    "associations": {
        "contactIds": [11877974],
        "companyIds": [ ],
        "dealIds": [ ],
        "ownerIds": [ ]
    },
    "attachments": [
        {
            "id": 4241968539
        }
    ],
    "metadata": {
        "body": "note body"
    }
})
headers = {
    'Content-Type': "application/json",
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)