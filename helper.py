from datetime import timezone
from dateutil.parser import parse
import pandas as pd
import simplejson
import json

###### metadata for payloads

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
def call_metadata(toNumber, fromNumber, status, durationMilliseconds, recordingURL, body):
    return {
        "toNumber" : toNumber,
        "fromNumber" : fromNumber,
        "status" : status,
        "durationMilliseconds" : durationMilliseconds,
        "recordingUrl" : recordingURL,
        "body" : body
    }

### tasks
def tasks_metadata():
    return {
        "body": "This is the body of the task.",
        "subject": "Task title",
        "status": "NOT_STARTED",
        "forObjectType": "CONTACT"
    }


####### Make Payload

### creating singular engagement dictionary payload  
def create_engagement(ownerID, type, time, metadata):
    {
        "engagement": {
            "active": 'true', #--
            "ownerId": 1, # Map User to ID // if user is no longer with us --> use Jose ID
            "type": type, #--
            "timestamp": time #--
        },
        "associations": { #### todo
            "contactIds": [11877974],
            "companyIds": [ ],
            "dealIds": [ ],
            "ownerIds": [ ]
        },
        ### optional
        # "attachments": [
        #     {
        #         "id": 4241968539
        #     }
        # ],
        "metadata": metadata
    }

####### Misc Helpers

### parse date into unix time for HS
def ISO_to_UNIX(d):
    dt = parse(d)
    return int(round(dt.replace(tzinfo=timezone.utc).timestamp(),0))


####### loading and viewing data

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

######## test functions 

def test():
    print(ISO_to_UNIX('2021-06-08T20:30:19.333000+00:00'))

if __name__ == "__main__":
    test()