import numpy as np
import pandas as pd
from credentials_connection import User

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
			print('Focus Areas Already Populated')

		else:
			for el in focus_area_lst:
				if(el in focus_str):
					self.focus_areas = self.focus_areas + el + ';'

		print('success')

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
		df = df.drop(['attributes'], axis = 1)
		return df
	
	def get_attenddess_after(self):
		query = "SELECT Id, Name, eb4sf__Event_Id__c, eb4sf__Email__c, eb4sf__First_Name__c, eb4sf__Last_Name__c, eb4sf__Account__c FROM eb4sf__Eventbrite_Order__c WHERE CreatedDate > " + self.date
		resp = self.sf.query_all(query)['records']
		df = pd.DataFrame(resp)
		df = df.drop(['attributes'], axis = 1)
		return df