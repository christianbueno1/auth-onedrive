import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"
# download path for any operating system
DOWNLOAD_PATH = os.path.expanduser("~/Downloads")

class ExcelFileGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        window_width = 700
        window_height = 400
        self.title("Excel File Selector")
        # self.geometry(f"{window_width}x{window_height}")

        # Calculate the position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(screen_width, screen_height)
        # ask to type enter
        # print("Press Enter to continue")
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the geometry with the calculated position
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Create and place the label
        label = ctk.CTkLabel(self, text="Select an Excel file to load", font=("Arial", 16))
        label.pack(pady=20)

        # Label for displaying the selected file path
        self.label = ctk.CTkLabel(self, text="No file selected", width=400)
        self.label.pack(pady=20)

        # Button to trigger file selection
        self.file_button = ctk.CTkButton(self, text="Select Excel File", command=self.select_file)
        self.file_button.pack(pady=20)

        # Button to load the Excel file into a DataFrame
        self.load_button = ctk.CTkButton(self, text="Load Excel File", command=self.load_excel, state="disabled")
        self.load_button.pack(pady=20)
    
    def select_file(self):
        # Open file dialog to select an Excel file
        file_path = filedialog.askopenfilename(
            initialdir=DOWNLOAD_PATH,
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


# define a run function to start the GUI event loop
def run():
    app = ExcelFileGUI()
    app.mainloop()