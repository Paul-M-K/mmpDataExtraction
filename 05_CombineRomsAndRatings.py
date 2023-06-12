import os
# import json
import pandas as pd
import roman
import re
import math
from fuzzywuzzy import fuzz

# Load the JSON file into a pandas DataFrame
games = pd.read_json('13_GameDirectory.json')
ratings = pd.read_json('14.3_GameRatingConsolesJoined.json')

# Drop duplicate data in both data frames
games = games.drop_duplicates()
ratings = ratings.drop_duplicates()


# Remove strings like (U) or (J)
games['Game'] = games['Game'].str.replace(r"\s*\([UJ]\)", '', regex=True)

# fix Pokemon for incoming ratings data
ratings['Game'] = ratings['Game'].str.replace("é", "e")

# make all lower case
games['Game'] = games['Game'].str.lower()
ratings['Game'] = ratings['Game'].str.lower()

# remove words like the
games['Game'] = games['Game'].str.replace("the ", " ")
ratings['Game'] = ratings['Game'].str.replace("the ", " ")

# replace & with and
games['Game'] = games['Game'].str.replace("&", "and")
ratings['Game'] = ratings['Game'].str.replace("&", "and")

# Define the characters to remove
characters_to_remove = r"!@#$%^*()-_=+[:;\"{,}].<>/?'"
games['Game'] = games['Game'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())
ratings['Game'] = ratings['Game'].apply(lambda x: re.sub(f"[{re.escape(characters_to_remove)}]", ' ', x).strip())


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

ratings['Game'] = ratings['Game'].apply(replace_roman_numerals)
games['Game'] = games['Game'].apply(replace_roman_numerals)

# remove all spaces 
games['Game'] = games['Game'].str.replace(' ', '')
ratings['Game'] = ratings['Game'].str.replace(' ', '')


# Merge the data frames based on matching values
merged_df = pd.merge(games, ratings, left_on=['Console', 'Console'], right_on=['Console', 'Console'])
merged_df = merged_df[merged_df['Game_x'].str[-1] == merged_df['Game_y'].str[-1]]

merged_df['similarity'] = merged_df.apply(lambda row: fuzz.ratio(row['Game_x'], row['Game_y']), axis=1)


# Sort the DataFrame by 'Game_y' and 'similarity' columns in descending order
similarity_df = merged_df.sort_values(['similarity'], ascending=[False])

similarity_df = similarity_df[similarity_df['similarity'] > 99]


# Keep only the first occurrence of each game's original name
similarity_df = similarity_df.drop_duplicates(subset='Directory', keep='first')


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

# Group the DataFrame by 'Console Name'
grouped = similarity_df.groupby('Console')

# Calculate the weighted average for each game within each console
for group_name, group_data in grouped:
    # print("Group:", group_name)
    
    weighted_df = pd.DataFrame(columns=['Directory','Original Name', 'rating', 'Weighted Average'])
    # Calculate the Wilson score for each game in the current group
    for index, row in group_data.iterrows():
        directory_name = row['Directory']
        game_name = row['Original Name']
        rating = row['rating']
        total_ratings = row['rating_count']
        
        weighted_ave = weighted_average(rating, total_ratings, group_data['rating_count'].sum())
        # Append the result to the group dataframe
        weighted_df = pd.concat([weighted_df, pd.DataFrame({'Directory': [directory_name],'Original Name': [game_name], 'rating': [rating], 'Weighted Average': [weighted_ave]})], ignore_index=True)

    # Store the group dataframe in the dictionary
    group_dataframes[group_name] = weighted_df


def rename_files(folder_path, old_file, new_name):
    # join the number and name back together
    # Get the old and new file paths

    old_path = os.path.join(folder_path, old_file)
    new_path = os.path.join(folder_path, new_name)

    # print(old_path)

    # # Check if the new file name already exists
    if os.path.exists(new_path):
        # File with the new name already exists, skip renaming
        return

    # Rename the file
    os.rename(old_path, new_path)

# Access and work with dataframes in the dictionary
for group_name, group_df in group_dataframes.items():
    # print("Group:", group_name)

    # Perform operations on the dataframe
    # For example, you can sort the dataframe by the Wilson Score column in descending order
    sorted_df = group_df.sort_values(by='Weighted Average', ascending=False)
    sorted_df = sorted_df.reset_index(drop=True)

    # Create a new column based on the updated index values
    sorted_df['New Rank'] = sorted_df.index.map(lambda x: str(x + 1).zfill(3))

    # Perform operations on the dataframe
    sorted_df['New Name and Rank'] = sorted_df['New Rank'] + ' ' + sorted_df['Original Name']

    for index, row in sorted_df.iterrows():
        directory = row['Directory'].rsplit('\\', 1)[0]
        old_name = row['Original Name']
        new_name = row['New Name and Rank']
        rename_files(directory,old_name,new_name)

