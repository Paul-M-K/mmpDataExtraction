import os
import json
import pandas as pd
import math
import re
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
    df = pd.DataFrame(data, columns=['Console Name', 'Game Name'])
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

# Duplicate Original File name for retaining data.
games['Original Name'] = games['Game Name']

# Drop duplicate data in both data frames
games = games.drop_duplicates()
ratings = ratings.drop_duplicates()

# remove any game type name like .gba, .zip... etc.
games['Game Name'] = games['Game Name'].apply(lambda x: x.rsplit(".", 1)[0])
games['Game Name'] = games['Game Name'].str.strip()

# Remove strings like (U) or (J)
games['Game Name'] = games['Game Name'].str.replace(r"\s*\([UJ]\)", '', regex=True)

# fix Pokemon for incoming ratings data
ratings['Game Name'] = ratings['Game Name'].str.replace("Ã©", "e")


# remove any odd characters.
# Define the characters to remove
characters_to_remove = r"!@#$%^&*()-_=+[:;\"{,}].<>/?'"
games['Game Name'] = games['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())
ratings['Game Name'] = ratings['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())

games.to_csv('games.csv', index=False)
ratings.to_csv('ratings.csv', index=False)

# Remove three-digit numbers from "Game Name" column
games['Game Name'] = games['Game Name'].apply(lambda x: x.split(maxsplit=1)[1] if len(x.split(maxsplit=1)[0]) == 3 and x.split(maxsplit=1)[0].isdigit() else x)
# print(games['Game Name'])
# games['Game Name'] = games['Game Name'].apply(lambda x: x.lstrip('0123456789') if x[:3].isdigit() else x)
# games['Game Name'] = games.apply(lambda row: row['Game Name'].lstrip('0123456789') if row['Game Name'][:3].isdigit() else row['Game Name'], axis=1)
# games.loc[games['Console Name'] == 'PS', 'Game Name'] = games.loc[games['Console Name'] == 'PS', 'Game Name'].apply(lambda x: x[:2] if len(x) == 2 else x)


# Merge the data frames based on matching values
merged_df = pd.merge(games, ratings, left_on=['Console Name', 'Console Name'], right_on=['Console Name', 'Console Name'])


# Define the characters to remove
# characters_to_remove = "!@#$%^&*()-_=+[:;\"{,}].<>/?"

# # Remove specific characters from the 'Game Name_y' column
# merged_df['Game Name_x'] = merged_df['Game Name_x'].str.replace(f"[{characters_to_remove}]", ' ', regex=True).str.strip()
# merged_df['Game Name_y'] = merged_df['Game Name_y'].str.replace(f"[{characters_to_remove}]", ' ', regex=True).str.strip()


# Calculate the similarity between the "Game" and "Game Name" columns

# def calculate_similarity(row):
#     if isinstance(row['Game Name_x'], str) and isinstance(row['Game Name_y'], str):
#         return fuzz.ratio(row['Game Name_x'], row['Game Name_y'])
#     else:
#         return math.nan

# merged_df['similarity'] = merged_df.apply(calculate_similarity, axis=1)

merged_df['similarity'] = merged_df.apply(lambda row: fuzz.ratio(row['Game Name_x'], row['Game Name_y']), axis=1)
merged_df.to_csv('merged_df.csv', index=False)
# Sort the DataFrame by 'similarity' column in descending order
sorted_df = merged_df.sort_values('similarity', ascending=False)
sorted_df = sorted_df[sorted_df['similarity'] > 60]
sorted_df.to_csv('sorted_df.csv', index=False)
print(sorted_df)

# Group the DataFrame by the unique combinations of 'Game Name_x' and 'Game Name_y'
grouped_df = sorted_df.groupby(['Game Name_x', 'Game Name_y'])
# print(grouped_df)

# Initialize an empty DataFrame to store the filtered results
filtered_df = pd.DataFrame(columns=sorted_df.columns)

# Iterate over the groups and keep the unique occurrences with the highest similarity
for group_name, group_data in grouped_df:
    max_similarity = group_data['similarity'].max()
    best_matches = group_data[group_data['similarity'] == max_similarity]
    filtered_df = pd.concat([filtered_df, best_matches], ignore_index=True)

# Print the filtered DataFrame
# print(filtered_df)
filtered_df.to_csv('filtered_df.csv', index=False)

# Filter the rows where similarity is above 95%
# similarity_df = sorted_df[merged_df['similarity'] > 60]

# Get the index of the first occurrence of each unique 'game_name_x'
# max_sim_indices = sorted_df.sort_values('Game Name_x',ascending=False)
# print(max_sim_indices)

# Filter the DataFrame to keep only the rows with the highest similarity
# filtered_df = similarity_df.loc[max_sim_indices]

# Print the updated DataFrame
# print(filtered_df)
# print(games)

# Print the filtered DataFrame
# filtered_df.to_csv('test.csv', index=False)
# print(merged_df)


