import os
import sys

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
                    
# def main():
#     selected_folder = sys.argv[1]  # Access the selected_folder value from command-line arguments
#     find_files(selected_folder)                    

# if __name__ == '__main__':
#     main()