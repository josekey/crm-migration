from datetime import time
from os import name
from typing import Text
from numpy import record
from helper import  email_metadata, meeting_metadata, call_metadata, tasks_metadata
from helper import ISO_to_UNIX, get_HS_id, create_engagement, initialize_global_spreadsheets
import logging

logging.basicConfig(filename='/Users/jose/Documents/program_projects/crm-migration/errors.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


# import_api key: api_5yFGuWzW1SmPepijoAc9w4.4ZKsvukTNwCJb5zKJhNh9b

initialize_global_spreadsheets()

#### create engagement payloads for each type
# collecting metadata for Hubspot APi call
def samson(data):
    # loop through companies

    engagements = []

    for row in data:
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
                        cont.append(temp)
                comp = get_HS_id(act['lead_id'], 'company')
                d = get_HS_id(act['lead_id'], 'deal')

                body = "",
                startTime = ISO_to_UNIX(act['starts_at']), ### unix time
                endTime = ISO_to_UNIX(act['ends_at']),
                title = act['title'],
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
                status = "COMPLETED",
                forObjectType = "COMPANY"

                metadata = tasks_metadata(body, subject, status, forObjectType)

                engagements.append(create_engagement(ownerID, type, time, metadata, comp))




# if __name__ == "__main__":
#     main()

############ NOTES ############

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
