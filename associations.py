from os import write
import pandas as pd
from helper import load_close, load_HS

def main():
    deals = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/stage1_clean/deals.xlsx')
    HS_d = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/from-HS/hubspot-crm-exports-all-deals-2021-08-09.xlsx')

    ids = HS_d.loc[:,['Deal Name', 'Deal ID']].rename(columns={'Deal Name': 'company name'}).drop_duplicates()

    print(ids.shape)
    print(deals.shape)

    linked = deals.set_index('company name').join(ids.set_index('company name'), how='left').drop_duplicates()    

    print(linked.shape)
    
    # linked.to_excel('/Users/jose/Documents/program_projects/crm-migration/test.xlsx')

def clean_fields_for_deals():
    deals = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_2_clean/deals_pipe.xlsx')

    deals.loc[deals['pipeline'] == 'Sales', 'pipeline'] = 'Sales Pipeline'
    deals.loc[deals['pipeline'] =='Brokers', 'pipeline'] = 'Broker Pipeline'

    deals.loc[deals['stage'] =='Set Made 10%', 'stage'] = 'Set Made'    
    deals.loc[deals['stage'] =='Set Held / Demoed 20%', 'stage'] = 'Set Held / Demoed' 
    deals.loc[deals['stage'] =='Quick Quote Sent 30%', 'stage'] = 'Quick Quote Sent'   
    deals.loc[deals['stage'] =='Census Received 40%', 'stage'] = 'Census Received'  
    deals.loc[deals['stage'] =='Final Quote Presented 50%', 'stage'] = 'Final Quote Presented'  
    deals.loc[deals['stage'] =='Quote Proposal Sent 90%', 'stage'] = 'Quote Proposal Sent'
    deals.loc[deals['stage'] =='Quote Proposal SIGNED - WON!', 'stage'] = 'Quote Proposal Signed'    
    

    deals.loc[deals['stage'] =='Quote Proposal SIGNED - WON!', 'stage'] = 'Quote Proposal Signed'
  

    deals.to_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_3_clean/clean_deals.xlsx', index=False)

def clean_fields_for_companies():
    comp = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_2_clean/companies.xlsx')

    comp.loc[comp['status'] == 'Potential', 'status'] = 'New'
    comp.loc[comp['status'] == 'Not Interested', 'status'] = 'Bad Timing'
    comp.loc[comp['status'] == 'Not Qualified', 'status'] = 'Unqualified'
    comp.loc[comp['status'] == 'Unsubscribe', 'status'] = 'Bad Timing'
    comp.loc[comp['status'] == 'Partner', 'status'] = 'Other'
    comp.loc[comp['status'] == 'Bad Lead', 'status'] = 'Bad Timing'
    comp.loc[comp['status'] == 'Customer', 'status'] = 'Connected'
    comp.loc[comp['status'] == 'LinkedIn Campaign', 'status'] = 'Marketing qualified lead'
    comp.loc[comp['status'] == 'Angle Advocate', 'status'] = 'Evangelist'
    comp.loc[comp['status'] == 'Cold Call', 'status'] = 'Sales qualified lead'
    comp.loc[comp['status'] == 'Email Campaign', 'status'] = 'Marketing qualified lead'
    comp.loc[comp['status'] == 'Event', 'status'] = 'Sales qualified lead'

    comp.loc[comp['is public'] == 'Privately Held', 'is public'] = 'Private'
    comp.loc[comp['is public'] == 'Public Company', 'is public'] = 'Public'

    comp.to_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_3_clean/clean_companies.xlsx')



def clean_fields_for_contacts():
    cont = pd.read_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_2_clean/contacts.xlsx')

    cont['stage'] = 'Lead'


    cont.loc[cont['status'] == 'Potential', 'status'] = 'New'
    cont.loc[cont['status'] == 'Not Interested', 'status'] = 'Bad Timing'
    cont.loc[cont['status'] == 'Not Qualified', 'status'] = 'Unqualified'
    cont.loc[cont['status'] == 'Unsubscribe', 'status'] = 'Bad Timing'
    cont.loc[cont['status'] == 'Partner', 'status'] = 'Other'
    cont.loc[cont['status'] == 'Partner', 'stage'] = 'Connected'
    cont.loc[cont['status'] == 'Bad Lead', 'status'] = 'Bad Timing'
    cont.loc[cont['status'] == 'Customer', 'status'] = 'Connected'
    cont.loc[cont['status'] == 'Customer', 'stage'] = 'Customer'
    cont.loc[cont['status'] == 'LinkedIn Campaign', 'status'] = 'Marketing qualified lead'
    cont.loc[cont['status'] == 'Angle Advocate', 'status'] = 'Evangelist'
    cont.loc[cont['status'] == 'Angle Advocate', 'stage'] = 'Connected'
    cont.loc[cont['status'] == 'Cold Call', 'status'] = 'Sales qualified lead'
    cont.loc[cont['status'] == 'Email Campaign', 'status'] = 'Marketing qualified lead'
    cont.loc[cont['status'] == 'Event', 'status'] = 'Sales qualified lead'

    cont.to_excel('/Users/jose/Documents/program_projects/crm-migration/data/Stage_3_clean/clean_contacts.xlsx')




def create_id_association_files():
    # company name, lead_id, HS_company_id
    # contact name, close_contact_id, HS_contact_id
    # deal name, opportunity_id, HS_deal_id

    # load hs content
    HS_contacts, HS_companies, HS_deals = load_HS()

    # load close
    close_cont, close_leads, close_opp = load_close()

    # contacts
    h = HS_contacts.loc[:,['Contact ID', 'First Name', 'Last Name']].rename(columns={'First Name':'first_name', 'Last Name':'last_name', 'Contact ID':'HS_cont_id'})
    c = close_cont.loc[:,['id', 'first_name', 'last_name']].rename(columns={'id':'close_cont_id'})

    contacts = h.merge(c, on=['first_name', 'last_name'], how='left')
    
    # companies
    h = HS_companies.loc[:,['Company ID', 'company name']].rename(columns={'Company ID':'HS_comp_id', 'company name':'company_name'})
    c = close_leads.loc[:,['id', 'display_name']].rename(columns={'id':'close_comp_id', 'display_name':'company_name'})

    companies = h.merge(c, on=['company_name'], how='left')

    # deals
    h = HS_deals.loc[:,['Deal ID', 'Deal Name']].rename(columns={'Deal ID':'HS_deal_id', 'Deal Name':'deal_name'})
    c = close_opp.loc[:,['id', 'lead_name']].rename(columns={'id':'close_deal_id', 'lead_name':'deal_name'})

    deals = h.merge(c, on=['deal_name'], how='left')

    # write to xlsx with multiple sheets
    with pd.ExcelWriter('/Users/jose/Documents/program_projects/crm-migration/id_associations.xlsx') as writer:
        contacts.to_excel(writer, sheet_name='contacts')
        companies.to_excel(writer, sheet_name='companies')
        deals.to_excel(writer, sheet_name='deals')



if __name__ == "__main__":
    create_id_association_files()