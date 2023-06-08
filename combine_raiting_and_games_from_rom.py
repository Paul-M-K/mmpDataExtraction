import os
import json
import pandas as pd
import roman
import math
import re
from spellchecker import SpellChecker
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
games = games[~games['Game Name'].str.endswith('.jpg')]
games['Game Name'] = games['Game Name'].apply(lambda x: x.rsplit(".", 1)[0])
games['Game Name'] = games['Game Name'].str.strip()

# Remove strings like (U) or (J)
games['Game Name'] = games['Game Name'].str.replace(r"\s*\([UJ]\)", '', regex=True)

# fix Pokemon for incoming ratings data
ratings['Game Name'] = ratings['Game Name'].str.replace("é", "e")

# remove words like the
games['Game Name'] = games['Game Name'].str.replace("the", " ")
ratings['Game Name'] = ratings['Game Name'].str.replace("the", " ")

# Define the characters to remove
characters_to_remove = r"!@#$%^&*()-_=+[:;\"{,}].<>/?'"
games['Game Name'] = games['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())
ratings['Game Name'] = ratings['Game Name'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())


def correct_spelling(input_string):
    spell_checker = SpellChecker()
    corrected_string = ""

    # Split the input string into individual words
    words = input_string.split()

    # Check and correct the spelling of each word
    for word in words:
        # Get the corrected version of the word if it is misspelled
        corrected_word = spell_checker.correction(word)

        # Check if a valid correction is found
        if corrected_word is not None:
            # Add the corrected word to the corrected string
            corrected_string += corrected_word + " "
        else:
            # If no valid correction is found, keep the original word
            corrected_string += word + " "

    # Remove the trailing space
    corrected_string = corrected_string.strip()

    return corrected_string

def convert_last_roman_to_number(string):
    parts = string.split()
    last_part = parts[-1]
    try:
        converted_part = str(roman.fromRoman(last_part))
        parts[-1] = converted_part
    except roman.InvalidRomanNumeralError:
        pass
    return ' '.join(parts)

def add_number_if_missing(string):
    # Check if the string ends with a number
    if not re.search(r'\d$', string):
        # Append "1" to the string
        string += "1"
    return string

ratings['Game Name'] = ratings['Game Name'].apply(correct_spelling)
games['Game Name'] = games['Game Name'].apply(correct_spelling)
ratings['Game Name'] = ratings['Game Name'].apply(convert_last_roman_to_number)
games['Game Name'] = games['Game Name'].apply(convert_last_roman_to_number)
games['Game Name'] = games['Game Name'].apply(add_number_if_missing)
ratings['Game Name'] = ratings['Game Name'].apply(add_number_if_missing)

games.to_csv('games.csv', index=False)
ratings.to_csv('ratings.csv', index=False)

# Remove three-digit numbers from "Game Name" column
games['Game Name'] = games['Game Name'].apply(lambda x: x.split(maxsplit=1)[1] if len(x.split(maxsplit=1)[0]) == 3 and x.split(maxsplit=1)[0].isdigit() else x)

# make an exeption for play station because it is only 2 numbers foe their naming convention.
games['Game Name'] = games.apply(lambda row: row['Game Name'].split(maxsplit=1)[1] if row['Console Name'] == 'PS' and len(row['Game Name'].split(maxsplit=1)[0]) == 2 and row['Game Name'].split(maxsplit=1)[0].isdigit() else row['Game Name'], axis=1)

# remove all spaces 
games['Game Name'] = games['Game Name'].str.replace(' ', '')
ratings['Game Name'] = ratings['Game Name'].str.replace(' ', '')

# make all lower case
games['Game Name'] = games['Game Name'].str.lower()
ratings['Game Name'] = ratings['Game Name'].str.lower()

# Merge the data frames based on matching values
merged_df = pd.merge(games, ratings, left_on=['Console Name', 'Console Name'], right_on=['Console Name', 'Console Name'])
merged_df = merged_df[merged_df['Game Name_x'].str[-1] == merged_df['Game Name_y'].str[-1]]


print(merged_df)

merged_df['similarity'] = merged_df.apply(lambda row: fuzz.ratio(row['Game Name_x'], row['Game Name_y']), axis=1)

# Sort the DataFrame by 'Game Name_y' and 'similarity' columns in descending order
sorted_df = merged_df.sort_values(['similarity'], ascending=[False])

# sorted_df = sorted_df[sorted_df['similarity'] > 99]

sorted_df.to_csv("sorted_df_original_name.csv", index=False)


# Keep only the first occurrence of each game's original name
filtered_df = sorted_df.drop_duplicates(subset='Original Name', keep='first')

filtered_df.to_csv('result_df.csv', index=False)


# merged_df = merged_df[merged_df['similarity'] > 0]
# merged_df.to_csv('merged_df.csv', index=False)
# # Sort the DataFrame by 'similarity' column in descending order
# sorted_df = merged_df.sort_values('similarity', ascending=False)
# sorted_df = sorted_df[sorted_df['similarity'] > 20]
# sorted_df.to_csv('sorted_df.csv', index=False)
# print(sorted_df)

# # Group the DataFrame by the unique combinations of 'Game Name_x' and 'Game Name_y'
# grouped_df = sorted_df.groupby(['Game Name_x', 'Game Name_y'])
# # print(grouped_df)

# # Initialize an empty DataFrame to store the filtered results
# filtered_df = pd.DataFrame(columns=sorted_df.columns)

# # Iterate over the groups and keep the unique occurrences with the highest similarity
# for group_name, group_data in grouped_df:
#     max_similarity = group_data['similarity'].max()
#     best_matches = group_data[group_data['similarity'] == max_similarity]
#     filtered_df = pd.concat([filtered_df, best_matches], ignore_index=True)

# # Print the filtered DataFrame
# # print(filtered_df)
# filtered_df.to_csv('filtered_df.csv', index=False)




