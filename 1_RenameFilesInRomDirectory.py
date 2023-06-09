import os
import re
import shutil

# will need to change this.
directory = "C:\\Users\\pauru\\Desktop\\Roms - Copy" 

def shift_directory(root, folder):
    src = os.path.join(root, folder)
    dst = os.path.dirname(root)
    shutil.move(src, dst)


#First we want to reorder the folders for Onion OS.
def move_folder(directory):
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            print(folder)
            # Move the folder one directory up
            if folder == 'CPS1+2' or folder == 'CPS3' or folder == 'GBC' or:
                shift_directory(root, folder)
                print(f'Folder: {folder}')
            else:
                print('skip')
            
            

print(move_folder(directory))

# def rename_files(directory):    
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             relative_path = os.path.relpath(file_path, directory)
#             folder_name = os.path.basename(relative_path)
            
#             # Count the number of backslashes in the file path
#             backslash_count = relative_path.count('\\')
            
#             if backslash_count > 1:
#                 # Split the relative path using backslashes
#                 parts = relative_path.split('\\')
                
#                 if "CPS1+2" in parts:
#                     # Get the index of "CPS1+2" in the parts list
#                     index = parts.index("CPS1+2")
#                     # Extract the console and game
#                     console = parts[1]
#                     game = parts[-1]
#                     data.append([console, game])

#                 elif "CPS3" in parts:
#                     # Get the index of "CPS3" in the parts list
#                     index = parts.index("CPS3")
#                     # Extract the console and game
#                     console = parts[1]
#                     game = parts[-1]
#                     data.append([console, game])

#                 elif "IGS" in parts:
#                     # Get the index of "IGS" in the parts list
#                     index = parts.index("IGS")
#                     # Extract the console and game
#                     console = parts[1]
#                     game = parts[-1]
#                     data.append([console, game])

#                 elif "EASYRPG" in parts:
#                     # Get the index of "IGS" in the parts list
#                     index = parts.index("EASYRPG")
#                     # Extract the console and game
#                     console = parts[0]
#                     game = parts[1]
#                     if game not in unique_games:
#                         unique_games.add(game)
#                         data.append([console, game])

#                 elif "GBC" in parts:
#                     # Check if ".jpg" is present in any part of the path
#                     if any(".jpg" in part for part in parts):
#                         continue
#                     # Get the index of "GBC" in the parts list
#                     index = parts.index("GBC")
#                     # Extract the console and game
#                     console = parts[1]
#                     game = parts[-1]
#                     data.append([console, game])
                    
#                 elif "PS" in parts:
#                     # Get the index of "PS" in the parts list
#                     index = parts.index("PS")
#                     # Extract the console and game
#                     console = parts[0]
#                     game = parts[1]
#                     if game not in unique_games:
#                         unique_games.add(game)
#                         data.append([console, game])

#                 else:
#                     # File path needs further parsing
#                     needs_parsing.append(relative_path)
                    
#             else:
#                 # Replace backslash with forward slash and split the file name into column and game parts
#                 parts = relative_path.replace('\\', '/').split('/')
#                 # Splitting the file path based on the last occurrence of '/'
#                 column = '/'.join(parts[:-1])
#                 game = parts[-1]
#                 data.append([column, game])