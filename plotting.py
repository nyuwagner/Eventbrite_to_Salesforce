import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

attendees = pd.read_csv('test.csv')
print(attendees.head())

print(len(attendees['eb4sf__Email__c'].unique()))

attendees['domain'] = ''

for index, row in attendees.iterrows():
    attendees.at[index,'domain'] = row['eb4sf__Email__c'].split('@')[1]

f = open("domains.json")
data = f.read().replace('\n', '')
domains = json.loads(data)

unique_domains = attendees[~attendees['domain'].isin(domains)]

print(len(unique_domains))
# for index, row in unique_domains.iterrows():
#     print(row['domain'])