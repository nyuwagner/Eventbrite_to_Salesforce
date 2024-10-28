import numpy as np
import pandas as pd
import json
from credentials_connection import User
import logging

event_logger = logging.getLogger(__name__)
logging.basicConfig(filename='event.log', encoding='utf-8', level=logging.INFO, filemode='w')

focus_area_lst = ['Cities', \
	'Communication Skills', \
	'Data Science and Data Management', \
	'Education', \
	'Environment, Climate Change, and Sustainability', \
	'Health', \
	'Inequality, Race, and Poverty', \
	'International Development', \
	'Nonprofits and Government', \
	'Philanthropy and Fundraising', \
	'Social Justice and Democracy', \
	'Transportation', \
	'Program Evaluation']

class Event:

	def __init__(self, event_id, name):
		self.name = name
		self.event_id = event_id
		self.focus_areas = ''

	def get_event_title(self):
		return(self.name)

	def get_focus_areas(self):
		return(self.focus_areas)

	def format_focus_areas(self, focus_str):
		if(focus_str != ''):
			logging.info('Focus Areas Already Populated')

		else:
			for el in focus_area_lst:
				if(el in focus_str):
					self.focus_areas = self.focus_areas + el + ';'

		logging.info('Focus Areas populated')

class EventList:

	def __init__(self, date):
		self.date = date
		conn = User('dev')
		conn.getCredentials()
		self.sf = conn.sf_login()

	def get_events_after(self):
		query = "SELECT Id, Name, eb4sf__Created__c, eb4sf__Description__c, eb4sf__Online_Event__c, Areas_of_Impact__c FROM eb4sf__Eventbrite_Event__c WHERE CreatedDate > " + self.date
		resp = self.sf.query_all(query)['records']
		df = pd.DataFrame(resp)
		df = df.rename(columns={"Name": "eb4sf__Event_Id__c"})
		df = df.drop(['attributes'], axis = 1)
		return df
	
	def get_attenddess_after(self):
		query = "SELECT Id, Name, eb4sf__Event_Id__c, eb4sf__Email__c, eb4sf__First_Name__c, eb4sf__Last_Name__c, eb4sf__Account__c FROM eb4sf__Eventbrite_Order__c WHERE CreatedDate > " + self.date
		resp = self.sf.query_all(query)['records']
		df = pd.DataFrame(resp)
		df = df.drop(['attributes'], axis = 1)
		return df

	def match_contacts(self, df):
		df['SF_ID'] = ''
		for index, row in df.iterrows():
			query = "SELECT Id, AccountId FROM Contact WHERE Email = '" + row['eb4sf__Email__c'] + "'"
			try:
				resp = self.sf.query_all(query)['records']
				if(len(resp)>0):
					df.at[index, 'SF_ID'] = resp[0]['Id']
			except Exception as e:
				logging.debug(e)
		
		return df[df['SF_ID'] != '']
	
	def match_domains(self, df):
		for index, row in df.iterrows():
			df.at[index,'domain'] = row['eb4sf__Email__c'].split('@')[1]

		f = open("domains.json")
		data = f.read().replace('\n', '')
		domains = json.loads(data)

		unique_domains = df[~df['domain'].isin(domains)]
		logging.info("### Unique Domains ###")
		logging.info(len(unique_domains))

		domain_dict = {}
		print(unique_domains.columns)

		for index, row in unique_domains.iterrows():
			#print(row['domain'])
			query = "SELECT Id, Number_of_Contacts_Plus_Related__c FROM Account WHERE Website like '%" + row['domain'] + "%' OR Domain__c = '" + row['domain'] + "'"
			try: 
				resp = self.sf.query_all(query)['records']
				if(len(resp)>0):
					max = 0
					for acc in resp:
						if(acc['Number_of_Contacts_Plus_Related__c'] > max):
							max = acc['Number_of_Contacts_Plus_Related__c']
							domain_dict.update({index: (acc['Id'], acc['Number_of_Contacts_Plus_Related__c'])})
			except Exception as e:
				logging.error("error: %s at index: %s", e, str(index))

		for key, value in domain_dict.items():
			unique_domains.at[key, 'AccountId'] = value[0]

		return unique_domains


