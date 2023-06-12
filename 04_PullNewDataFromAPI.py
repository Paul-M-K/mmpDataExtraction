# imports
import requests
import time
import json
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Read the environment variables
client_id = os.getenv('CLIENT_ID')
access_token = os.getenv('ACCESS_TOKEN')

# Define the file path
input_file_path = '14.1_ConsoleDataIGDB.json'
output_file_path = '14.2_GameRatingIGDB.json'

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

    # print(response.json())
    # Append the response data to the combined list
    combined_list.append(response.json())
    time.sleep(0.25)

# Flatten the combined response to remove the outer brackets
flattened_response = [item for sublist in combined_list for item in sublist]

# Write the flattened response to the output JSON file
with open(output_file_path, 'w') as file:
    json.dump(flattened_response, file, indent=4)

# Load game data from JSON file
with open(output_file_path) as game_file:
    game_data = json.load(game_file)

# print(platforms_data)
# Create an empty list to store the matching game data
matching_games_list = []

# Iterate through console data
for console in platforms_data:
    console_id = console['id']
    console_name = console['alternative_name']
    matching_games = [game for game in game_data if console_id in game['platforms']]

    # Append the matching game data to the list
    for game in matching_games:
        platform = [p for p in game['platforms'] if p == console_id]
        if platform:
            matching_games_list.append({
                'ID': console_id,
                'Console': console_name,
                'Game': game['name'],
                'rating': game['rating'],
                'rating_count': game['rating_count']
            })

# Create a DataFrame from the matching game data list
df = pd.DataFrame(matching_games_list)

# Iterate over unique groups
for group_value in df['ID'].unique():
    group_data = df[df['ID'] == group_value]  # Extract the data for the current group

# Sort the DataFrame by 'ValueColumn' in descending order while keeping the groups intact
df_sorted = df.sort_values(by=['ID'], ascending=[True])

# Remove duplicate rows based on all columns
df_no_duplicates = df_sorted.drop_duplicates()
print(df_no_duplicates)

# # Save the DataFrame to a json file
df_no_duplicates.to_json('14.3_GameRatingConsolesJoined.json', orient='records')
df_no_duplicates.to_csv('14.3_GameRatingConsolesJoined.csv')