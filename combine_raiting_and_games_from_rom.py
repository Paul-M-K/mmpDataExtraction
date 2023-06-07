import os
import json
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from fuzzywuzzy import fuzz

# will need to change this.
directory = "C:\\Users\\pauru\\Desktop\\My Folder\\miyoo mini\\Roms" 

def parse_data(directory):
    data = []
    needs_parsing = []
    unique_games = set()  # Set to store unique games
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            folder_name = os.path.basename(relative_path)
            
            # Count the number of backslashes in the file path
            backslash_count = relative_path.count('\\')
            
            if backslash_count > 1:
                # Split the relative path using backslashes
                parts = relative_path.split('\\')
                
                if "CPS1+2" in parts:
                    # Get the index of "CPS1+2" in the parts list
                    index = parts.index("CPS1+2")
                    # Extract the console and game
                    console = parts[1]
                    game = parts[-1]
                    data.append([console, game])

                elif "CPS3" in parts:
                    # Get the index of "CPS3" in the parts list
                    index = parts.index("CPS3")
                    # Extract the console and game
                    console = parts[1]
                    game = parts[-1]
                    data.append([console, game])

                elif "IGS" in parts:
                    # Get the index of "IGS" in the parts list
                    index = parts.index("IGS")
                    # Extract the console and game
                    console = parts[1]
                    game = parts[-1]
                    data.append([console, game])

                elif "EASYRPG" in parts:
                    # Get the index of "IGS" in the parts list
                    index = parts.index("EASYRPG")
                    # Extract the console and game
                    console = parts[0]
                    game = parts[1]
                    if game not in unique_games:
                        unique_games.add(game)
                        data.append([console, game])

                elif "GBC" in parts:
                    # Check if ".jpg" is present in any part of the path
                    if any(".jpg" in part for part in parts):
                        continue
                    # Get the index of "GBC" in the parts list
                    index = parts.index("GBC")
                    # Extract the console and game
                    console = parts[1]
                    game = parts[-1]
                    data.append([console, game])
                    
                elif "PS" in parts:
                    # Get the index of "PS" in the parts list
                    index = parts.index("PS")
                    # Extract the console and game
                    console = parts[0]
                    game = parts[1]
                    if game not in unique_games:
                        unique_games.add(game)
                        data.append([console, game])

                else:
                    # File path needs further parsing
                    needs_parsing.append(relative_path)
                    
            else:
                # Replace backslash with forward slash and split the file name into column and game parts
                parts = relative_path.replace('\\', '/').split('/')
                # Splitting the file path based on the last occurrence of '/'
                column = '/'.join(parts[:-1])
                game = parts[-1]
                data.append([column, game])

        # Create DataFrame from the parsed data
    df = pd.DataFrame(data, columns=['Console', 'Game'])
    return df, needs_parsing


parsed_data, paths_needing_parsing = parse_data(directory)

parsed_data.to_json('parsed_games_for_rating.json', orient='records')

# match games in directory to ratings in json file.
# use a try catch to find all relivent data.

# Define the file path
games_file_path = 'parsed_games_for_rating.json'
ratings_file_path = 'games_rating_console_joined.json'

# read json file
with open(games_file_path) as games_file:
    games_data = json.load(games_file)

# read json file
with open(ratings_file_path) as ratings_file:
    ratings_data = json.load(ratings_file)

# Convert json to df.
games = pd.DataFrame(games_data)
ratings = pd.DataFrame(ratings_data)
games['Game'] = games['Game'].str.split('.').str[0]


# Assuming you have the "games" and "ratings" DataFrames
# Merge the DataFrames based on Console and Game columns

# Create an empty list to store the merged records
merged_records = []
df = pd.DataFrame()
# Iterate over the rows in the "games" DataFrame
for console_abbr in games['Console'].unique():
    group_data = df[games['Console'] == console_abbr]
    print(group_data)
    # print(console)
# for index, game_row in games.iterrows():
#     console = game_row['Console']
#     game = game_row['Game']

    
#     # Find the best match in the "ratings" DataFrame based on similarity
#     best_match = None
#     best_similarity = 0

    # if ratings['Console Name'] == console:
    #     print('yes')
    
    # for index, rating_row in ratings.iterrows():
    #     console_name = rating_row['Console Name']
    #     print(console_name)
    #     game_name = rating_row['Game Name']
        
#         # Calculate the similarity score between the game and game_name
#         similarity = fuzz.token_set_ratio(game, game_name)
        
#         # Check if the similarity score is above the threshold
#         if similarity > 90 and similarity > best_similarity:
#             best_match = rating_row
#             best_similarity = similarity
    
#     # If a match is found, append the merged record to the list
#     if best_match is not None:
#         merged_record = pd.concat([game_row, best_match])
#         merged_records.append(merged_record)

# # Create the merged DataFrame from the list of merged records
# merged_df = pd.DataFrame(merged_records)

# # Display the merged DataFrame
# print(merged_df)


