import customtkinter as ctk

class GridExampleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the grid rows and columns
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expand with window
        self.grid_columnconfigure(1, weight=1)  # Make column 1 expand with window
        self.grid_rowconfigure(0, weight=1)     # Make row 0 expand with window
        self.grid_rowconfigure(1, weight=1)     # Make row 1 expand with window

        # Create widgets and place them in the grid
        self.label = ctk.CTkLabel(self, text="Label 1", fg_color="white")
        self.label.grid(row=0, column=0, padx=85, pady=10, sticky="nsew")

        self.button = ctk.CTkButton(self, text="Button")
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter text")
        self.entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


# Main application
if __name__ == "__main__":
    app = GridExampleApp()
    app.geometry("300x200")
    app.mainloop()
