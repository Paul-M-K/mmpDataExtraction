import os
import pandas as pd

# will need to change this.
directory = "C:\\Users\\pauru\\Desktop\\Roms-reduced - Copy" 

def game_dataframe(directory):
    data = []
    needs_parsing = []
    unique_games = set()  # Set to store unique games
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
                        directory = (f'{root}\{folder}\{file}')
                        data.append([directory, folder, file])
    df = pd.DataFrame(data, columns=['Directory', 'Console', 'Game'])
    return df

df = game_dataframe(directory)

# Clean dataframe
# Drop duplicates based on all columns
df.drop_duplicates(inplace=True)

strings_to_drop = ['.jpg','Imgs', '_libretro', '.cfg','.smsplus' ]

#drop all unneeded strings
for string in strings_to_drop:
    df = df[~df['Game'].str.contains(string)]


df.to_csv('Directory_Games.csv', index=False)

