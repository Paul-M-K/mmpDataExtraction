import os
import shutil
import sys

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
            

# def main():
#     selected_folder = sys.argv[1]  # Access the selected_folder value from command-line arguments
#     move_folder(selected_folder)

# if __name__ == '__main__':
#     main()

