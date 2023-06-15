import os
import pandas as pd
import sys

    
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

    df.to_json('13_GameDirectory.json', orient='records')

    
# def main():


# if __name__ == '__main__':
#     main()

