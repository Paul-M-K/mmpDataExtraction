from requests import post
import time
import json
import os

# will need to change this.
folder = "C:\\Users\\pauru\\source\\GBATest" 

for file in os.listdir(folder):
    file_split = file.split(".gba")
    print(file_split)
    if file_split.find('Pokemon') in file_split:
        print(file_split)
    # game_name = file_split[0].replace("-", ": ")
    # game_name = game_name.replace("-", ":")
    # print(file_split[0])
    # response = post('https://api.igdb.com/v4/games/',**{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm','Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},'data': 'fields rating, rating_count, name, platforms; where name = "{}";'.format(game_name)}).text
    # print("file Name: ", game_name, " response: ",response)
    # time.sleep(0.25)

'''
response = post('https://api.igdb.com/v4/platforms/', **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm', 'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},'data': 'fields *; where name = "Nintendo Entertainment System"; limit 500;'}).text

# print ("response: %s" % str(response.json()))

print(response)

for i in data:
    consoleName = str(i['name'])
    response = post('https://api.igdb.com/v4/platforms/',
                    **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm',
                                   'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},
                       'data': 'fields *; where name = "{}";'.format(consoleName)})
    # print(response)
    write_json(response.json())
'''

