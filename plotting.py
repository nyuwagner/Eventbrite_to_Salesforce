import numpy as np
import pandas as pd

attendees = pd.read_csv('test.csv')
print(attendees.head())

print(len(attendees['eb4sf__Email__c'].unique()))

attendees['domain'] = ''

for index, row in attendees.iterrows():
    attendees.at[index,'domain'] = row['eb4sf__Email__c'].split('@')[1]

no_nyu = attendees[attendees['domain'] != 'nyu.edu']
no_gmail = no_nyu[no_nyu['domain'] != 'gmail.com']

print(len(no_gmail))
for index, row in no_gmail.iterrows():
    print(row['domain'])