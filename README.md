# Miyoo Mini Plus Data Extraction, Transformation and Integration.
## Introduction
The [Miyoo Mini Plus](https://www.keepretro.com/products/miyoo-mini-plus) (MMP) is a handheld retro gaming console that offers a collection of 6000+ games (For the 64GB model) from various retro consoles, compatible with the [RetroArch](https://www.retroarch.com/) platform. While the MMP is highly regarded as a fantastic handheld device, there is a notable issue: the games are not organized effectively. This lack of organization bothers me and I want to resolve this issue. In this project, the primary focus is to tackle this issue and provide a solution.

## Goals

1) [X] Generate a list of games for the Miyoo Mini Plus:
A comprehensive list of games for the 64GB can be accessed [here](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FPaul-M-K%2FmmpDataExtraction%2Fmaster%2Fparsed_data.xlsx&wdOrigin=BROWSELINK).

2) [X] Reorganize games based on user ratings:
The main objective of this project is to reorganize the games and rank them based on user ratings obtained from [IGBD](https://www.igdb.com/) (Internet Game Database).

3) [X]  Sort games into correct folders for [Onion OS](https://github.com/OnionUI/Onion):
The games will be sorted into the appropriate folders within Onion OS. Although this process is relatively quick, there may be certain anomalies to address, such as the Game Boy Color folder being located within the Game Boy folder.

4) turn this into a small application so anyone can download the executable file and run their game library through it.

By achieving these goals, I aim to enhance the user experience of the Miyoo Mini Plus by ensuring that the vast game library is properly organized and easily accessible.

## Data Extraction
**Step 1** was relatively simple to perform. I utilized Python and the OS module to create a code that traversed the directory of the Miyoo Mini Plus Roms folder. This code effectively sorted each game based on its directory structure. For instance, if the file path was "G:\Roms\SNES\Fake Game Name.zip," the code would identify the console as SNES and label the game as Fake Game Name.zip. However, there were some exceptions due to the presence of several subfolders. To handle these exceptions, if statements were implemented to facilitate folder parsing.

You can access an Excel file containing all the game names included with the Miyoo Mini Plus 64GB model [here](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2FPaul-M-K%2FmmpDataExtraction%2Fmaster%2Fparsed_data.xlsx&wdOrigin=BROWSELINK). Please note that this file specifically lists the game names and does not include the actual game files.

## Data Integration
1) I want to use the excel file that was created to Pull all the Console data from the API. 
- Get id numbers for all consoles.
2) Use console id and game name to get user rating and rating count. 


## Notes for me.

mmp_RenameFilesForApiCalls is only functioning with a Test file, not the original roms folder. This will need to be modified so it can directly look at the roms folder. 
