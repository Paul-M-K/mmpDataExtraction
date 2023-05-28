import json
import time
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the environment variables
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')

# Define the file paths
input_file_path = 'platforms.json'
output_file_path = 'platformsDataextract.json'

# Load the platforms data from the input JSON file
with open(input_file_path) as file:
    platforms_data = json.load(file)

# Create an empty list to store the combined responses
combined_list = []

# Iterate over the platforms data
for platform in platforms_data:
    console_name = platform['name']
    
    # Make a request to the IGDB API to retrieve platform details
    url = 'https://api.igdb.com/v4/platforms'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    data = f'fields *; where name = "{console_name}";'
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    time.sleep(0.25)
    
    # Append the response data to the combined list
    combined_list.append(response.json())

# Flatten the combined response to remove the outer brackets
flattened_response = [item for sublist in combined_list for item in sublist]

# Write the flattened response to the output JSON file
with open(output_file_path, 'w') as file:
    json.dump(flattened_response, file, indent=4)