import PySimpleGUI as sg
import subprocess

def run_gui():
    # Define the layout of your GUI
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

def main():
    # Execute GUI.py and capture the selected folder
    selected_folder = run_gui()

    # Pass the selected_folder to other scripts using subprocess
    # For example, to execute another script, you can use:
    subprocess.run(["python", "MoveFoldersUpOneDirectory.py", selected_folder])
    subprocess.run(["python", "RenameRomsWithNumbersInFront.py", selected_folder])
    subprocess.run(["python", "CreateJSONFromRoms.py", selected_folder])
    subprocess.run(["python", "CombineRomsAndRatings.py"])

    # Display a message after all subprocesses have finished
    sg.popup('All processes have finished.')

if __name__ == '__main__':
    main()
