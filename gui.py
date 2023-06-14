import PySimpleGUI as sg
import subprocess

def main():
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

    # Close the window
    window.close()

    # Access the selected folder as a string
    selected_folder = values["-FOLDER-"]

    # Execute main.py and pass selected_folder as a command-line argument
    # subprocess.run(["python", "main.py", selected_folder])

if __name__ == '__main__':
    main()