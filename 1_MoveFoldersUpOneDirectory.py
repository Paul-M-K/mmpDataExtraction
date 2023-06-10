import os
import shutil

# will need to change this.
directory = "C:\\Users\\pauru\\Desktop\\Roms-reduced - Copy"

# we will use this definition to move the folders up one directory level.


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
            


move_folder(directory)
