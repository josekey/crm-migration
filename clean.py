from os import name
from typing import Text
from numpy import record
from helper import ISO_to_UNIX, make_activity_json, email_metadata, meeting_metadata, call_metadata, tasks_metadata
import pandas as pd
import json
import simplejson


# import_api key: api_5yFGuWzW1SmPepijoAc9w4.4ZKsvukTNwCJb5zKJhNh9b

def main():
    make_activity_json('Rbm Building Services')

#### create engagement payloads for each type
# collecting metadata for Hubspot APi call
def samson(data):
    # loop through companies
    for row in data:
        # pull activity data
        activities = row['activities']

        # loop through activities
        for act in activities:
            # general activity information 
            timestamp = ISO_to_UNIX(act['activity_at'])
            user = act["user_name"]

            # if email
            if act['_type'] == 'Email':
                type = 'EMAIL'

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
            
            # if meeting
            elif act['_type'] == 'Meeting':
                type = 'MEETING'

                body = "",
                startTime = ISO_to_UNIX(act['starts_at']), ### unix time
                endTime = ISO_to_UNIX(act['ends_at']),
                title = act['title'],
                internalMeetingNotes = act['note']

                meeting_metadata(body, startTime, endTime, title, internalMeetingNotes)

            # if note
            elif act['_type'] == 'Note':
                type = 'NOTE'

                {'body':act['note']}

            # if call
            elif act['_type'] == 'Call':
                type = "CALL"

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

                call_metadata(toNumber, fromNumber, status, durationMilliseconds, recordingUrl, body)

            # if task
            elif act["_type"] == "TaskCompleted":
                body = act['task_text']
                subject = "Imported Task"
                status = "COMPLETED",
                forObjectType = "COMPANY"

                tasks_metadata(body, subject, status, forObjectType)



if __name__ == "__main__":
    main()

############ NOTES ############

# mappings for users, contact, companies, and deals to HubSpot ID

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

