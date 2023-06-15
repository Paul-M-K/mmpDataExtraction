"""
This module contains functions for performing specific tasks.
"""

import os
import shutil
import re
import roman
import PySimpleGUI as sg
import pandas as pd

# import math
from fuzzywuzzy import fuzz

def run_gui():
    """
    This will run the GUI
    Args:
        No arguments requires.
    Returns:
        the result is the selected folder for where the roms are stored.
    """
    layout = [
        [sg.Text("Select a folder:")],
        [sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Button("Submit")]
    ]

    # Create the window
    window = sg.Window("Folder Selection", layout)

    # Event loop to process events and get folder selection
    while True:
        event, values = window.read()

        # If the window is closed or "Submit" button is clicked, exit the loop
        if event == sg.WINDOW_CLOSED or event == "Submit":
            break

        # Update the input field with the selected folder
        if event == "FolderBrowse":
            folder = values["-FOLDER-"]
            window["-FOLDER-"].update(folder)

    # Access the selected folder as a string
    selected_folder = values["-FOLDER-"]

    return selected_folder

## --- MoveFoldersUpOneDirectory ---

def shift_directory(root, folder):
    src = os.path.join(root, folder)
    dst = os.path.dirname(root)
    shutil.move(src, dst)

# First we want to reorder the folders for Onion OS.
# assuming this file pattern is the same for all Miyoo Mini Plus 64 gb.
def move_folder(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            # Move the folder one directory up
            if folder == 'CPS1+2' or folder == 'CPS3' or folder == 'GBC':
                shift_directory(root, folder)


## --- RenameRomsWithNumbersInFront ---

def lead_number_removal(parts, type):
    #
    #
    #
    # Need look for digits.
    #
    #
    #
    if type == 3 and len(parts[0]) == 3:
        parts.pop(0)
        return parts
    elif type == 2 and len(parts[0]) == 2:
        parts.pop(0)
        return parts
    else:
        return parts
    
def rename_files(folder_path, old_file, name):
    # join the number and name back together
    # Get the old and new file paths
    new_name = ' '.join(name)
    old_path = os.path.join(folder_path, old_file)
    new_path = os.path.join(folder_path, new_name)

    # Check if the new file name already exists
    if os.path.exists(new_path):
        # File with the new name already exists, skip renaming
        return

    # Rename the file
    os.rename(old_path, new_path)


# Now I want to rename all the different Roms inside their respective folder. 
# for example 001 Pokemon Fire Red, should just be Pokemon Fire Red.
def find_files(directory):
    # list of console in the roms folder
    consoles = ['FC', 'GB', 'GBC', 'GBA', 'GG', 'MD', 'NGP', 'PCE', 'SFC', 'WS']
    ps = 'PS'

    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            # Move the folder one directory up
            folder_path = os.path.join(root, folder)
            for file in os.listdir(folder_path):
                # Loop through all the console and folders.
                for folder_name in consoles:
                    # Check if the folder name matches the current console.
                    # split the files into their parts
                    parts = file.split(" ", 1)
                    if folder == folder_name:
                        # check for leading numbers
                        name = lead_number_removal(parts, 3)
                        # rename the files
                        rename_files(folder_path, file, name)
                    elif folder == ps:
                        # check for leading numbers
                        name = lead_number_removal(parts, 2)
                        # rename the files
                        rename_files(folder_path, file, name)

## --- CreateJSONFromRoms ---
 
def game_dataframe(directory):
    data = []
    # needs_parsing = []
    # unique_games = set()  # Set to store unique games
    # list of console in the roms folder
    consoles = ['FC', 'GB', 'GBC', 'GBA', 'GG', 'MD', 'NGP', 'PCE', 'SFC', 'WS', 'PS']
    
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            for file in os.listdir(folder_path):
                # Loop through all the console and folders.
                for folder_name in consoles:
                    # Check if the folder name matches the current console.
                    # split the files into their parts
                    if folder == folder_name:
                        # check for leading numbers
                        root = root.replace("/", "\\")
                        directory = (root+"\\"+folder+"\\"+file)
                        data.append([directory, folder, file, file])
    df = pd.DataFrame(data, columns=['Directory', 'Console', 'Original Name', 'Game'])
    
    # Clean dataframe
    # Drop duplicates based on all columns
    df.drop_duplicates(inplace=True)
    # df["Directory"] = df["Directory"].str.replace("\\", "",regex=False)
    strings_to_drop = ['.jpg','Imgs', '_libretro', '.cfg','.smsplus' ]

    #drop all unneeded strings
    for string in strings_to_drop:
        df = df[~df['Game'].str.contains(string)]

    df['Game'] = df['Game'].apply(lambda x: x.rsplit(".", 1)[0])
    df['Game'] = df['Game'].str.strip()

    # df.to_json('13_GameDirectory.json', orient='records')
    return df

## --- CombineRomsAndRatings ---

def merge(df):
    # Load the JSON file into a pandas DataFrame
    # games = pd.read_json('13_GameDirectory.json')
    games = pd.DataFrame(df)
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
    
    
    # def wilson_score(rating, total_ratings, z=1.96):
    #     # Check if total_ratings is zero
    #     if total_ratings == 0:
    #         return 0  # Return a score of 0 when total_ratings is zero
        
    #     # Calculate the proportion of positive ratings
    #     positive_proportion = rating / 100
        
    #     # Calculate the Wilson score interval
    #     expr = positive_proportion * (1 - positive_proportion) + z * z / (4 * total_ratings)
    #     sqrt_expr = math.sqrt(expr) if expr >= 0 else 0
        
    #     score = (positive_proportion + z*z / (2*total_ratings) - z * sqrt_expr) / (1 + z*z / total_ratings)
        
    #     return score
    
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
    
        # # Check if the new file name already exists
        if os.path.exists(new_path):
            # File with the new name already exists, skip renaming
            return
    
        # Rename the file
        os.rename(old_path, new_path)
    
    # Access and work with dataframes in the dictionary
    for group_name, group_df in group_dataframes.items():
    
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

def main():
    # Execute GUI.py and capture the selected folder
    selected_folder = run_gui()

    move_folder(selected_folder)
    find_files(selected_folder)
    df = pd.DataFrame(game_dataframe(selected_folder))
    merge(df)

    # Display a message after all subprocesses have finished
    sg.popup('All processes have finished.')

if __name__ == '__main__':
    main()
