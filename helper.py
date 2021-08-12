from datetime import timezone
from dateutil.parser import parse
from numpy import e
import pandas as pd
import simplejson
import json
import logging

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
def tasks_metadata(body, subject, status, forObjectType):
    return {
        "body": body,
        "subject": subject,
        "status": status,
        "forObjectType": forObjectType
    }


####### Make Payload

### creating singular engagement dictionary payload  
def create_engagement(ownerID, type, time, metadata, contacts=[], companies=[], deals=[]):
    {
        "engagement": {
            "active": 'true', #--
            "ownerId": ownerID, # Map User to ID // if user is no longer with us --> use Jose ID
            "type": type, #--
            "timestamp": time #--
        },
        "associations": { #### todo --> all arrays
            "contactIds": contacts,
            "companyIds": companies,
            "dealIds": deals,
            "ownerIds": []
        },
        ### optional
        # "attachments": [
        #     {
        #         "id": 4241968539
        #     }
        # ],
        "metadata": metadata # dictionary
    }


####### loading and viewing data

def load_close():
    #load close data
    contacts = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health contacts 2021-08-05 18-30.csv')
    leads = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health leads 2021-08-05 18-30.csv')
    opportunities = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health opportunities 2021-08-05 18-30.csv')
    
    return contacts, leads, opportunities

def load_HS():
    #load close data
    contacts = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/from-HS/hubspot-crm-exports-all-contacts-2021-08-11.xlsx')
    companies = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/from-HS/hubspot-crm-exports-all-companies-2021-08-08.xlsx')
    deals = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/from-HS/hubspot-crm-exports-all-deals-2021-08-11.xlsx')
    
    return contacts, companies, deals


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

####### Misc Helpers

def initialize_global_spreadsheets():
    global contacts, companies, deals, rep

    # id associations between close and HS
    xlsx = pd.ExcelFile('/Users/jose/Documents/program_projects/crm-migration/id_associations.xlsx')
    contacts = pd.read_excel(xlsx, 'contacts')
    companies = pd.read_excel(xlsx, 'companies')
    deals = pd.read_excel(xlsx, 'deals')

    # hubspot user IDs
    rep = {'James Fakult': 1456,
            'Justin Turner': 485,
            'Dallas Thompson': 1970,
            'Jared Steele': 453,
            }

    

###
def get_HS_id(name, t): 
    try:
        if t == 'contact':
            return [contacts.loc[contacts['close_cont_id'] == name, 'HS_cont_id'].values[0]]
        elif t == 'company':
            return [companies.loc[companies['close_comp_id'] == name, 'HS_comp_id'].values[0]]
        elif t == 'deal':
                d = companies.loc[companies['close_comp_id'] == name, 'company_name'].values[0] 
                return [deals.loc[deals['deal_name'] == d, 'HS_deal_id']]
        
        ### get owner ID --> default to Jose for non active members --> 2
        elif t == 'owner':
            try:
                return rep[name]
            except KeyError:
                return 2
    except e:
        logging.error(f'{t} association not found for {name}')

    return []


### parse date into unix time for HS
def ISO_to_UNIX(d):
    dt = parse(d)
    return int(round(dt.replace(tzinfo=timezone.utc).timestamp(),0))

######## test functions 

def test():
    initialize_global_spreadsheets()
    print(get_HS_id('lead_grEGHEd0KbBcO4LjkJasD56iBDMdT6snUvRYm8JmMAb', 'company'))

if __name__ == "__main__":
    test()