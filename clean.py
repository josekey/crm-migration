from os import name
from typing import Text
from numpy import record
from helper import ISO_to_UNIX
import pandas as pd
import json
import simplejson


# import_api key: api_5yFGuWzW1SmPepijoAc9w4.4ZKsvukTNwCJb5zKJhNh9b

def main():
    make_activity_json('Rbm Building Services')

    # populated = []
    # for i in range(0, len(data)):
    #     if data[i]['tasks'] or data[i]['activities']:
    #         populated.append(data[i])

    # print(len(populated))
    # df = pd.DataFrame(data=populated)
    # df.to_csv('/Users/jose/Documents/program_projects/pdf_render/clean1.csv')



    ### sample with data
    # temp = df.loc[df['name'] == 'BAER WELDING', :].to_dict()
    # print(df.loc[df['name'] == 'Gauzy', ])

    

    # print(type(temp))

    # print(temp['activities'])
    ### loop through the line items and display contacts 
    # l = len(data)
    # for i in range(0,l):
    #     data[i]['contact']

    
        
    ## prind all of the fields for one entry
    # temp = data[0]
    # for key in temp:
    #     input('Enter')
    #     print(f'{key}: {temp[key]}\n')   
    
    
    #load close data

    ## ad content to 'url' in leads
    ## associate leads(companies) and deals based on company name

#### create engagement payloads for each type
# collecting metadata for Hubspot APi call
def samson(data):
    # loop through companies
    for row in data:
        # pull activity data
        activities = row['activities']

        # loop through activities
        for act in activities:
            # if email
            if act['_type'] == 'Email':
                env = act['envelope']
                f = {'email':env['from'][0]['email'],
                        'firstName':env['from'][0]['name'].split()[0],
                        'lastName':env['from'][0]['name'].split()[-1]}
                to = f"{env['sender'][0]['name']} <{env['sender'][0]['email']}>"
                cc = act['cc']
                bcc = act['bcc']
                html = act['body_html']
                text = act['body_text']
                subject = env['subject']

                email_metadata(f, to, cc, bcc, subject, html, text)
            
            #if meeting
            elif act['_type'] == 'Meeting':
                body = "",
                startTime = ISO_to_UNIX(act['starts_at']), ### unix time
                endTime = ISO_to_UNIX(act['ends_at']),
                title = act['title'],
                internalMeetingNotes = act['note']

                meeting_metadata(body, startTime, endTime, title, internalMeetingNotes)

            elif act['_type'] == 'Note':
                {'body':act['note']}

            elif act['_type'] == 'Call':
                "toNumber" : "5618769964",
                "fromNumber" : "(857) 829-5489",
                "status" : "COMPLETED",
                "durationMilliseconds" : 38000,
                "recordingUrl" : act['recording_url'],
                "body" : ""



### note metadata type already created

### email    
def email_metadata(f, to, cc, bcc, subject, html, text):
    return {
        "from": f,
        "to": [to],
        "cc": cc,
        "bcc": bcc,
        "subject": subject, 
        "html": html, #"body_html"
        "text": text #'body_text'
    }

### meeting
def meeting_metadata(body, startTime, endTime, title, internalMeetingNotes):
    return {
        "body": body,
        "startTime": startTime, ### unix time
        "endTime": endTime,
        "title": title,
        "internalMeetingNotes" : internalMeetingNotes
    }

### call
def call_metadata():
    return {
        "toNumber" : "5618769964",
        "fromNumber" : "(857) 829-5489",
        "status" : "COMPLETED",
        "durationMilliseconds" : 38000,
        "recordingUrl" : "https://api.twilio.com/2010-04-01/Accounts/AC890b8e6fbe0d989bb9158e26046a8dde/Recordings/RE3079ac919116b2d22",
        "body" : ""
    }
        
### creating singular engagement dictionary payload  
def create_engagement(ownerID, type, time, metadata):
    {
        "engagement": {
            "active": 'true',
            "ownerId": 1,
            "type": type,
            "timestamp": time # unix
        },
        "associations": {
            "contactIds": [11877974],
            "companyIds": [ ],
            "dealIds": [ ],
            "ownerIds": [ ]
        },
        ### optional
        "attachments": [
            {
                "id": 4241968539
            }
        ],
        "metadata": metadata
    }


def load_close():
    #load close data
    contacts = pd.read_csv('/Users/jose/Documents/program_projects/CRM_clean/Close/Angle Health contacts 2021-08-05 18-30.csv')
    leads = pd.read_csv('/Users/jose/Documents/program_projects/CRM_clean/Close/Angle Health leads 2021-08-05 18-30.csv')
    opportunities = pd.read_csv('/Users/jose/Documents/program_projects/CRM_clean/Close/Angle Health opportunities 2021-08-05 18-30.csv')
    
    return contacts, leads, opportunities


### save beaufified json with activity for one company
def make_activity_json(company):
    f = open('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health leads 2021-08-09 21-39.json')
    data = json.load(f)

    df = pd.DataFrame(data=data)

    # temp = df.loc[df['name'] == 'BAER WELDING', 'activities'].to_dict()
    temp = df.loc[df['name'] == company, 'activities'].to_dict()

    # save beautified activities for specific company 
    savefile = open(f'/Users/jose/Documents/program_projects/crm-migration/{company}.json','w')
    savefile.write(simplejson.dumps(simplejson.loads(json.dumps(temp)), indent=4, sort_keys=True))
    savefile.close()


if __name__ == "__main__":
    main()