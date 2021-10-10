from datetime import time
from tqdm import tqdm
from os import name
from typing import Text
from numpy import record
from helper import  email_metadata, meeting_metadata, call_metadata, tasks_metadata
from helper import ISO_to_UNIX, get_HS_id, create_engagement, initialize_global_spreadsheets, save_json, format_cc_bcc
import logging
import json

logging.basicConfig(filename='/Users/jose/Documents/program_projects/crm-migration/errors.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


initialize_global_spreadsheets()


def main():
    # f = open('/Users/jose/Documents/program_projects/crm-migration/Close/Angle Health leads 2021-08-09 21-39.json')
    f = open('/Users/jose/Documents/program_projects/crm-migration/data/Close_Final/Angle Health leads 2021-08-12 03-38.json')

    data = json.load(f)

    print('Data Loaded\n\nRunning...')

    samson(data)



#### create engagement payloads for each type
# collecting metadata for Hubspot APi call
def samson(data):
    # loop through companies

    engagements = []

    for row in tqdm(data):
        # pull activity data
        activities = row['activities']

        # loop through activities
        for act in activities:
            # general activity information 
            time = ISO_to_UNIX(act['activity_at'])
            ownerID =  get_HS_id(act["user_name"], 'owner')

            # if email
            if act['_type'] == 'Email':
                type = 'EMAIL'

                # respective HS ids
                cont = get_HS_id(act['contact_id'], 'contact')
                comp = get_HS_id(act['lead_id'], 'company')
                d = get_HS_id(act['lead_id'], 'deal')


                # envelope contents
                env = act['envelope']

                # 'from' information
                try:
                    first = env['from'][0]['name'].split()[0]
                except:
                    logging.warning(f'EMAIL: first name not available for cont={cont} // comp={comp}')
                    first = ""
                try:
                    last = env['from'][0]['name'].split()[-1]
                except:
                    logging.warning(f'EMAIL: first name not available for cont={cont} // comp={comp}')
                    last = ""
                try:
                    last = env['from'][0]['name'].split()[-1]
                except:
                    logging.warning(f'EMAIL: first name not available for cont={cont} // comp={comp}')
                    last = ""

                try:
                    email = env['from'][0]['email']
                except:
                    email = ""
                try:
                    t = f"{env['to'][0]['name']} <{env['to'][0]['email']}>"
                except:
                    t = ""

               
                f = {'email': email,
                        'firstName':first,
                        'lastName':last}
                to = {'email': t}
                cc = format_cc_bcc(act['cc'])
                bcc = format_cc_bcc(act['bcc'])
                html = act['body_html']
                text = act['body_text']

                try:
                    subject = env['subject']
                except:
                    subject = ""

                metadata = email_metadata(f, to, cc, bcc, subject, html, text)

                engagements.append(create_engagement(ownerID, type, time, metadata, cont, comp, d))
            
            # if meeting
            elif act['_type'] == 'Meeting':
                type = 'MEETING'
                
                # respective HS ids
                cont = []
                for c in act['attendees']:
                    temp =  get_HS_id(c['contact_id'], 'contact')
                    if temp:
                        cont.append(temp[0])
                comp = get_HS_id(act['lead_id'], 'company')
                d = get_HS_id(act['lead_id'], 'deal')

                body = ""
                startTime = ISO_to_UNIX(act['starts_at']) ### unix time
                endTime = ISO_to_UNIX(act['ends_at'])
                title = act['title']
                internalMeetingNotes = act['note']

                metadata = meeting_metadata(body, startTime, endTime, title, internalMeetingNotes)

                engagements.append(create_engagement(ownerID, type, time, metadata, cont, comp, d))


            # if note
            elif act['_type'] == 'Note':
                type = 'NOTE'

                # respective HS ids
                cont = get_HS_id(act['contact_id'], 'contact')
                comp = get_HS_id(act['lead_id'], 'company')
                d = get_HS_id(act['lead_id'], 'deal')

                metadata = {'body':act['note']}

                engagements.append(create_engagement(ownerID, type, time, metadata, cont, comp, d))


            # if call
            elif act['_type'] == 'Call':
                type = "CALL"

                # respective HS ids
                cont = get_HS_id(act['contact_id'], 'contact')
                comp = get_HS_id(act['lead_id'], 'company')
                d = get_HS_id(act['lead_id'], 'deal')

                # metadata 
                if act['direction'] == 'outbound':
                    toNumber = act['phone']
                    fromNumber = act["local_phone"]
                else:
                    fromNumber = act['phone']
                    toNumber = act["local_phone"]

                status = "COMPLETED"
                durationMilliseconds = act['duration']*1000

                if act["has_recording"]:
                    recordingUrl = act['recording_url']
                else: 
                    recordingUrl = ""

                body = act["note"]

                metadata = call_metadata(toNumber, fromNumber, status, durationMilliseconds, recordingUrl, body)

                engagements.append(create_engagement(ownerID, type, time, metadata, cont, comp, d))


            # if task
            elif act["_type"] == "TaskCompleted":
                type = 'TASK'

                comp = get_HS_id(act['lead_id'], 'company')


                body = act['task_text']
                subject = "Imported Task"
                status = "COMPLETED"
                forObjectType = "COMPANY"

                metadata = tasks_metadata(body, subject, status, forObjectType)

                engagements.append(create_engagement(ownerID, type, time, metadata, companies=comp))


    save_json('/Users/jose/Documents/program_projects/crm-migration/data/PAYLOAD.json',engagements)


if __name__ == "__main__":
    main()

############ NOTES ############

# why are things populating in a list
# mappings for users, contact, companies, and deals to HubSpot ID, and Close ID
# func for owner Id

################# JUNK ############

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

