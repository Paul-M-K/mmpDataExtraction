# imports
from requests import post
import time
import json
import os
import matplotlib as plt

# need to use platforms data extraction id's to get a list off all the raitings for all their associated games. 

#platform data
with open('platformsDataextract.json', 'r') as f:
  data = json.load(f)

print(data['platform_details']['id'])


for i in data:
    consoleId = str(i['id'])
    print(consoleId)
    response = post('https://api.igdb.com/v4/platforms/',
                    **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm',
                                   'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},
                       'data': 'fields name, rating, rating_count; sort rating desc; where rating != null & platforms = "{}";'.format(consoleId)})


# import pandas as pd

# df = pd.read_json('platformsDataextract.json')

# print(df.to_string(['id'])) 
