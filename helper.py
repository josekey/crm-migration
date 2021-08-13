from datetime import timezone
from dateutil.parser import parse
from numpy import e
import pandas as pd
import simplejson
import json
import logging
import requests

########### metadata for payload #########

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


########## Make Payload ############

### creating singular engagement dictionary payload  
def create_engagement(ownerID, type, time, metadata, contacts=[], companies=[], deals=[]):
    return {
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


########### loading and viewing data ############

def load_close():
    #load close data
    contacts = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/data/Close_Final/Angle Health contacts 2021-08-12 00-37.csv')
    leads = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/data/Close_Final/Angle Health leads 2021-08-12 00-36.csv')
    opportunities = pd.read_csv('/Users/jose/Documents/program_projects/crm-migration/data/Close_Final/Angle Health opportunities 2021-08-12 00-37.csv')
    
    return contacts, leads, opportunities

def load_HS():
    #load close data
    contacts = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/HubSpot_Final/hubspot-crm-exports-all-contacts-2021-08-12.xlsx')
    companies = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/HubSpot_Final/hubspot-crm-exports-all-companies-2021-08-12.xlsx')
    deals = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/HubSpot_Final/hubspot-crm-exports-all-deals-2021-08-12.xlsx')
    
    return contacts, companies, deals


############### save beaufified json with activity ############
def make_activity_json(company):
    f = open('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health leads 2021-08-09 21-39.json')
    data = json.load(f)

    df = pd.DataFrame(data=data)

    # temp = df.loc[df['name'] == 'BAER WELDING', 'activities'].to_dict()
    temp = df.loc[df['name'] == company, 'activities'].to_dict()

    # save beautified activities for specific company 
    save_json(f'/Users/jose/Documents/program_projects/crm-migration/{company}.json',temp)
    

def save_json(filepath, contents):
    savefile = open(filepath,'w')
    savefile.write(simplejson.dumps(simplejson.loads(json.dumps(contents)), indent=4, sort_keys=True))
    savefile.close()

############ Misc Helpers ################

def initialize_global_spreadsheets():
    global contacts, companies, deals, rep

    # id associations between close and HS
    xlsx = pd.ExcelFile('/Users/jose/Documents/program_projects/crm-migration/id_associations.xlsx')
    contacts = pd.read_excel(xlsx, 'contacts')
    companies = pd.read_excel(xlsx, 'companies')
    deals = pd.read_excel(xlsx, 'deals')

    # hubspot user IDs
    rep = {'James Fakult': 95632221,
            'Justin Turner': 95632231,
            'Dallas Thompson': 95632220,
            'Jared Steele': 93445904,
            }

def format_cc_bcc(arg):
    if arg:
        return [ {'email': temp} for temp in arg]
    else: return[]


### returns list with HS ID
def get_HS_id(name, t): 
    try:
        if t == 'contact':
            return [int(contacts.loc[contacts['close_cont_id'] == name, 'HS_cont_id'].values[0])]
        elif t == 'company':
            return [int(companies.loc[companies['close_comp_id'] == name, 'HS_comp_id'].values[0])]
        elif t == 'deal':
                d = companies.loc[companies['close_comp_id'] == name, 'company_name'].values[0] 
                return [int(deals.loc[deals['deal_name'] == d, 'HS_deal_id'])]
        
        ### get owner ID --> default to Jose for non active members --> 2
        elif t == 'owner':
            try:
                return rep[name]
            except KeyError:
                return 93148800
    except:
        logging.warning(f'ASSOCIATION: {t} association not found for {name}')

    return []


### parse date into unix time for HS
def ISO_to_UNIX(d):
    dt = parse(d)
    return int(round(dt.replace(tzinfo=timezone.utc).timestamp(),0))


########### Post Migration #############

## creates json of engagements which fails to pass
def unpassed_json():
    ## error data
    f = open('/Users/jose/Documents/program_projects/crm-migration/api-records-1.log', 'r')
    lines = f.readlines()
    f.close()

    ## original payload
    f = open('/Users/jose/Documents/program_projects/crm-migration/data/PAYLOAD.json')
    data = json.load(f)
    f.close()

    ## loop through each line and get index
    indices = [int(line.split('-')[-1].split()[0]) for line in lines]

    ## find bad engagements using lins of indices
    engagements = [data[i] for i in indices]

    ## save
    save_json('/Users/jose/Documents/program_projects/crm-migration/data/failed.json',engagements)
        
def get_owner_name(id):
    querystring = {"hapikey":"97c5dee7-a000-4588-84fd-e3b6f4b44c24"}
    url = f"http://api.hubapi.com/owners/v2/owners/{id}?hapikey=97c5dee7-a000-4588-84fd-e3b6f4b44c24"
    response = requests.request('GET',url)

    temp = response.json()

    print(f'{temp["firstName"]} {temp["lastName"]}')




############ test functions #############

def test():
    # initialize_global_spreadsheets()
    # print(get_HS_id('lead_grEGHEd0KbBcO4LjkJasD56iBDMdT6snUvRYm8JmMAb', 'company'))

    # unpassed_json()

    get_owner_name(95632221)

    # print(format_cc_bcc(['jose@anglehealth.com', 'sours@dough.edu']))

if __name__ == "__main__":
    test()