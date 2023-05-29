# imports
import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the environment variables
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')

# Define the file path
input_file_path = 'platformsDataextract.json'
output_file_path = 'gamerating.json'

# Load the platformsdataextract data from the input JSON file
with open(input_file_path) as file:
    platforms_data = json.load(file)

# Create an empty list to store the combined responses
combined_list = []

# Iterate over the platforms data
for platform in platforms_data:
    platformId = platform['id']
    # Make a request to the IGDB API to retrieve game rating details
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    data = f'fields name, rating, rating_count, platforms; sort rating desc; where rating != null & platforms = [{platformId}]; limit 500;'
    response = requests.post(url, headers=headers, data=data)

    print(response.json())
    # Append the response data to the combined list
    combined_list.append(response.json())

# Flatten the combined response to remove the outer brackets
flattened_response = [item for sublist in combined_list for item in sublist]

# Write the flattened response to the output JSON file
with open(output_file_path, 'w') as file:
    json.dump(flattened_response, file, indent=4)