import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# Function to load the selected Excel file
def load_excel_file():
    # Open a file dialog for selecting the Excel file
    # Set the default download directory
    default_download_directory = os.path.expanduser("~/Downloads")

    file_path = filedialog.askopenfilename(
        title="Select Excel file",
        initialdir=default_download_directory,
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            messagebox.showinfo("Success", f"File loaded successfully!\n{file_path}")
            print(df.head())  # Print first few rows of the dataframe for verification
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the file.\n{str(e)}")

# Create the main window
app = ctk.CTk()
app.geometry("400x200")
app.title("Excel File Loader")

# Create and place the label
label = ctk.CTkLabel(app, text="Select an Excel file to load", font=("Arial", 16))
label.pack(pady=20)

# Create and place the button for selecting the Excel file
button = ctk.CTkButton(app, text="Browse", command=load_excel_file)
button.pack(pady=10)

# Start the GUI event loop
def run():
    app.mainloop()

