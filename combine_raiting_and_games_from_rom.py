import os
import json
import pandas as pd
import roman
import re
import enchant
import math
from spellchecker import SpellChecker
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from fuzzywuzzy import fuzz

# will need to change this.
directory = "C:\\Users\\pauru\\Desktop\\My Folder\\miyoo mini\\Roms" 

# Initialize the spell checker keep for furture referance
# spell_checker = enchant.Dict("en_US")

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

# Remove three-digit numbers from "Game Name" column
games['Game Name'] = games['Game Name'].apply(lambda x: x.split(maxsplit=1)[1] if len(x.split(maxsplit=1)[0]) == 3 and x.split(maxsplit=1)[0].isdigit() else x)

# make an exeption for play station because it is only 2 numbers foe their naming convention.
games['Game Name'] = games.apply(lambda row: row['Game Name'].split(maxsplit=1)[1] if row['Console Name'] == 'PS' and len(row['Game Name'].split(maxsplit=1)[0]) == 2 and row['Game Name'].split(maxsplit=1)[0].isdigit() else row['Game Name'], axis=1)

# Duplicate Original File name for retaining data.
games['Original Name'] = games['Game Name']
# ratings['Original Name'] = ratings['Game Name']

# Drop duplicate data in both data frames
games = games.drop_duplicates()
ratings = ratings.drop_duplicates()

# remove any game type name like .gba, .zip... etc.
games = games[~games['Game Name'].str.endswith('.jpg')]
games['Game Name'] = games['Game Name'].apply(lambda x: x.rsplit(".", 1)[0])
games['Game Name'] = games['Game Name'].str.strip()

# Remove strings like (U) or (J)
games['Game Name'] = games['Game Name'].str.replace(r"\s*\([UJ]\)", '', regex=True)

# fix Pokemon for incoming ratings data
ratings['Game Name'] = ratings['Game Name'].str.replace("é", "e")

# make all lower case
games['Game Name'] = games['Game Name'].str.lower()
ratings['Game Name'] = ratings['Game Name'].str.lower()

# remove words like the
games['Game Name'] = games['Game Name'].str.replace("the ", " ")
ratings['Game Name'] = ratings['Game Name'].str.replace("the ", " ")

# replace & with and
games['Game Name'] = games['Game Name'].str.replace("&", "and")
ratings['Game Name'] = ratings['Game Name'].str.replace("&", "and")

# Define the characters to remove
characters_to_remove = r"!@#$%^*()-_=+[:;\"{,}].<>/?'"
games['Game Name'] = games['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())
ratings['Game Name'] = ratings['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())

games.to_csv('games.csv', index=False)
ratings.to_csv('ratings.csv', index=False)

# Remove three-digit numbers from "Game Name" column
games['Game Name'] = games['Game Name'].apply(lambda x: x.split(maxsplit=1)[1] if len(x.split(maxsplit=1)[0]) == 3 and x.split(maxsplit=1)[0].isdigit() else x)

# make an exeption for play station because it is only 2 numbers foe their naming convention.
games['Game Name'] = games.apply(lambda row: row['Game Name'].split(maxsplit=1)[1] if row['Console Name'] == 'PS' and len(row['Game Name'].split(maxsplit=1)[0]) == 2 and row['Game Name'].split(maxsplit=1)[0].isdigit() else row['Game Name'], axis=1)

# Keep for future referance.
# Function to replace misspelled words in a text
# def replace_misspelled(text):
#     words = text.split()
#     corrected_words = []
#     for word in words:
#         if not spell_checker.check(word):
#             suggestions = spell_checker.suggest(word)
#             if suggestions:
#                 corrected_word = suggestions[0]
#             else:
#                 corrected_word = word
#         else:
#             corrected_word = word
#         corrected_words.append(corrected_word)
#     return ' '.join(corrected_words)

def replace_roman_numerals(sentence):
    words = sentence.split()

    updated_words = []
    for word in words:
        try:
            number = roman.fromRoman(word.upper())
            updated_words.append(str(number))
        except roman.InvalidRomanNumeralError:
            updated_words.append(word)

    updated_sentence = ' '.join(updated_words)
    return updated_sentence

ratings['Game Name'] = ratings['Game Name'].apply(replace_roman_numerals)
games['Game Name'] = games['Game Name'].apply(replace_roman_numerals)

# remove all spaces 
games['Game Name'] = games['Game Name'].str.replace(' ', '')
ratings['Game Name'] = ratings['Game Name'].str.replace(' ', '')


# Merge the data frames based on matching values
merged_df = pd.merge(games, ratings, left_on=['Console Name', 'Console Name'], right_on=['Console Name', 'Console Name'])
merged_df = merged_df[merged_df['Game Name_x'].str[-1] == merged_df['Game Name_y'].str[-1]]


merged_df['similarity'] = merged_df.apply(lambda row: fuzz.ratio(row['Game Name_x'], row['Game Name_y']), axis=1)

# Sort the DataFrame by 'Game Name_y' and 'similarity' columns in descending order
sorted_df = merged_df.sort_values(['similarity'], ascending=[False])

sorted_df = sorted_df[sorted_df['similarity'] > 99]

# Keep only the first occurrence of each game's original name
filtered_df = sorted_df.drop_duplicates(subset='Original Name', keep='first')

# filtered_df.to_csv('result_df.csv', index=False)
# filtered_df.to_json('games_raiting_matched_sililarity_100.json', orient='records')

# print(filtered_df)

# Group the DataFrame by 'Console Name'
grouped = filtered_df.groupby('Console Name')

def wilson_score(rating, total_ratings, z=1.96):
    # Check if total_ratings is zero
    if total_ratings == 0:
        return 0  # Return a score of 0 when total_ratings is zero
    
    # Calculate the proportion of positive ratings
    positive_proportion = rating / 100
    
    # Calculate the Wilson score interval
    expr = positive_proportion * (1 - positive_proportion) + z * z / (4 * total_ratings)
    sqrt_expr = math.sqrt(expr) if expr >= 0 else 0
    
    score = (positive_proportion + z*z / (2*total_ratings) - z * sqrt_expr) / (1 + z*z / total_ratings)
    
    return score

def weighted_average(rating, rating_count, total_ratings):
    weight = rating_count / total_ratings
    weighted_avg = rating * weight
    return weighted_avg

# Create an empty dictionary to store the dataframes
group_dataframes = {}

# Calculate the weighted average for each game within each console
for group_name, group_data in grouped:
    # print("Group:", group_name)
    
    group_df = pd.DataFrame(columns=['Original Name', 'rating', 'Weighted Average'])
    # Calculate the Wilson score for each game in the current group
    for index, row in group_data.iterrows():
        game_name = row['Original Name']
        rating = row['rating']
        total_ratings = row['rating_count']
        
        weighted_ave = weighted_average(rating, total_ratings, group_data['rating_count'].sum())
        # Append the result to the group dataframe
        group_df = pd.concat([group_df, pd.DataFrame({'Original Name': [game_name], 'rating': [rating], 'Weighted Average': [weighted_ave]})], ignore_index=True)
        
        # print("Game:", game_name)
        # print("Wilson Score:", weighted_ave)
        # print("---")

    # Store the group dataframe in the dictionary
    group_dataframes[group_name] = group_df

# Access and work with dataframes in the dictionary
for group_name, group_df in group_dataframes.items():
    print("Group:", group_name)

    # Perform operations on the dataframe
    # For example, you can sort the dataframe by the Wilson Score column in descending order
    sorted_df = group_df.sort_values(by='Weighted Average', ascending=False)
    sorted_df = sorted_df.reset_index(drop=True)

    # Create a new column based on the updated index values
    sorted_df['New Rank'] = sorted_df.index.map(lambda x: str(x + 1).zfill(3))

    # Perform operations on the dataframe
    sorted_df['New Name and Rank'] = sorted_df['New Rank'] + ' ' + sorted_df['Original Name']

    # Print the sorted dataframe
    print("Sorted", group_name, "DataFrame:")
    print(sorted_df)
    print("---")

# print(sorted_dataframes)


