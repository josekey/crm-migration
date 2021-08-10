# This example a local file named 'test_import.csv'
# This file contains a list of contact records to import.

import requests
import json
import os

# insert your api key here
url = "https://api.hubapi.com/crm/v3/imports?hapikey={{}}"

data = {
    "name": "test_import",
    "files": [
        {
            "fileName": "test_import.csv",
            "fileFormat": "SPREADSHEET",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                    {
                        "ignored": False,
                        "columnName": "First Name",
                        "idColumnType": None,
                        "propertyName": "firstname",
                        "foreignKeyType": None,
                        "columnObjectType": "CONTACT",
                        "associationIdentifierColumn": False
                    },
                    {
                        "ignored": False,
                        "columnName": "Email",
                        "idColumnType": "HUBSPOT_ALTERNATE_ID",
                        "propertyName": "email",
                        "foreignKeyType": None,
                        "columnObjectType": "CONTACT",
                        "associationIdentifierColumn": False
                    }
                ]
            }
        }
    ]}

datastring = json.dumps(data)

payload = {"importRequest": datastring}

current_dir = os.path.dirname(__file__)
relative_path = "./test_import.csv"

absolute_file_path = os.path.join(current_dir, relative_path)

files = [
    ('files', open(absolute_file_path, 'r'))
]
print(files)


response = requests.request("POST", url, data=payload, files=files)

print(response.text.encode('utf8'))
print(response.status_code)
