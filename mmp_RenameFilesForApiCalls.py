import os

# will need to change this.
folder = "C:\\Users\\pauru\\source\\GBATest" 

for file in os.listdir(folder):
    # split file names into a list
    file_split = file.split(" ")
    try:
        #check to make sure the first string can be converted to an int. (this is typical for MMP)
        type(int(file_split[0])) == int
        # check the length of the string, it is always 001 for example.
        if len(file_split[0]) == 3:
            # pop the number off
            popped = file_split.pop(0)
            # join the strings back together without the number
            name_split = ' '.join(map(str,file_split))
            # get old path and old name. 
            old_file = os.path.join(folder,file)
            # get old path and new name.
            new_file = os.path.join(folder,name_split)
            # check if the file does not exist
            if not os.path.exists(new_file):
                # rename game.
                os.rename(old_file, new_file)
    except ValueError:
        # Can't look at files with out the exeptions above so skip.
        print("Not an int")

    