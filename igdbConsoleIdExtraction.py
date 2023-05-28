# Here I want to use the API to call all the names in platforms.json.
# I want to create a new json file that will collect all relivent information for
# each console

from requests import post
import json
import os
import pandas as pd

# Opening JSON file
f = open('platforms.json')

# returns JSON objects as a dictionary
data = json.load(f)

# Define the file path and name
file_path = 'platformsDataextract.json'

# # Check if the file exists
if not os.path.exists(file_path):
    # Create the file and write an empty JSON structure
    with open(file_path, 'w') as file:
        json.dump({}, file)

# # # Open the file in write mode and write data
with open(file_path, 'w') as file:
    # Your data to be written into the JSON file
    dataDump = {'platform_details': []}
    json.dump(dataDump, file)


# function to add to JSON
def write_json(new_data, filename=file_path):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["platform_details"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

# iterating though the json list

combined_list = []
for i in data:
    consoleName = str(i['name'])
    response = post('https://api.igdb.com/v4/platforms/',
                    **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm',
                                   'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},
                       'data': 'fields *; where name = "{}";'.format(consoleName)})
    combined_list.append(response.json())
    # test = pd.DataFrame(pd.json_normalize(response.json()))
    # print(test.to_json())
    
    # print(response)
    # write_json(test.to_json().json())
# print(combined_list)
# Flatten the combined response to remove the outer brackets
flattened_response = [item for sublist in combined_list for item in sublist]
# Convert the flattened response to JSON format
json_data = json.dumps(flattened_response)
print(json_data)
write_json(json_data)


# print(consoleDict)

f.close()
# print(response)