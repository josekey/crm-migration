####################################
HS Configuration
####################################

# Object Mappings:
Close  >>  HubSpot
Contacts >> Contacts
Leads >> companies
Opportunities >> Deals

######### Beginning of Steps ##########

1. download from Close:
> Contact, Lead, Opportunity .csv files
> Lead .json file with call, meeting, email, and task history
> put into the data/Close folder

2. Manually copy relevant fields into respective xlsx files
> store in data/Stage_2_clean 

3. use functions in associations.py to clean field contents
> make compatible with HubSpot field types
> store in data/Stage_3_clean

4. Import files for data/Stage_3_clean into hubspot
> import two files at a time with assocaition on company name
> re-download one recently uploaded file from HS in order to to get hubspot IDs
> import last file allong with the redownloaded file --> association based on company name
> make sure to check box 'update by hubspot ID' in order to not duplicate objects of the reuploaded file

5. Download Contacts, companies, and deals from hubspot to get all hubspot IDs
> store in data/HubSpot_Final

6. Run create_id_association_files() from associations.py
> assocaitions stored in id_associations.xlsx in project root directory

7. Run sisyphus.py to pull engagements from the close .json
> reformated into HS compatible payload with HS ids for association
> errors.log will store warning --> assocaited deal, company, or contact ID not found
>>> means that close data does not have relevant information

8. Run engagement.py 
> api calls to HS with formatted payload
> errors logged in api-records.log along with respective index of failed engagment in the large payload file


((((iff errors in api-records.log))))

9. from helper.py, run unpassed_json()
> make json file of unpassed engagements
> manually look for errors
> check payload readabiliy against sample-api-calls.txt


