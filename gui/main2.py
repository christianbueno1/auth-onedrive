import customtkinter as ctk
from tkinter import filedialog, Tk
import pandas as pd
import os

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"


class ExcelFileGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Excel File Selector")
        self.geometry("500x200")

        # Label for displaying the selected file path
        self.label = ctk.CTkLabel(self, text="No file selected", width=400)
        self.label.pack(pady=20)

        # Button to trigger file selection
        self.file_button = ctk.CTkButton(self, text="Select Excel File", command=self.select_file)
        self.file_button.pack(pady=20)

        # Button to load the Excel file into a DataFrame
        self.load_button = ctk.CTkButton(self, text="Load Excel File", command=self.load_excel, state="disabled")
        self.load_button.pack(pady=20)

        # Variable to store the selected file path
        self.file_path = None

    def select_file(self):
        # Set the default download directory
        default_download_directory = os.path.expanduser("~/Downloads")
        # Open file dialog to select an Excel file
        file_path = filedialog.askopenfilename(
            initialdir=default_download_directory,
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            self.file_path = file_path
            self.label.configure(text=f"Selected: {file_path}")
            self.load_button.configure(state="normal")  # Enable the Load button

    def load_excel(self):
        if self.file_path:
            # Load the selected Excel file into a DataFrame using pandas
            try:
                df = pd.read_excel(self.file_path)
                print("Excel file loaded successfully!")
                print(df.head())  # Display the first few rows of the DataFrame
            except Exception as e:
                print(f"Error loading Excel file: {e}")
        else:
            print("No file selected.")


# Main application
if __name__ == "__main__":
    # Create the root window
    root = ExcelFileGUI()

    # Run the app
    root.mainloop()
