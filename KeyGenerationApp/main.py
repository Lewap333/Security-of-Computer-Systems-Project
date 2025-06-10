##
# @file main.py
# @brief Main application class for the Digital Signature Tool GUI.
#
# Initializes the main application window using customtkinter,
# and manages switching between different frames (views).

import customtkinter as ctk
from UI.generate_keys_frame import GenerateKeysFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

##
# @brief Main application class for the GUI.
#
# Handles frame management and sets up the main window's layout.
class MainApp(ctk.CTk):
    ##
    # @brief Initializes the main application window.
    #
    # Sets the window size, centers it, and initializes the first frame.
    def __init__(self):
        super().__init__()

        # Initial settings
        self.iconbitmap("icon.ico")
        self.title("Digital signature tool")
        self.window_width = 800
        self.window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Centering window on screen
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Load initial frame
        self.frames["GenerateKeysFrame"] = GenerateKeysFrame(self.container, controller=self)
        self.frames["GenerateKeysFrame"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("GenerateKeysFrame")

    ##
    # @brief Displays a specific frame by name.
    #
    # @param page_name The name of the frame to display.
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    ##
    # @brief Returns the width of the application window.
    #
    # @return Window width in pixels.
    def get_width(self):
        return self.window_width

    ##
    # @brief Returns the height of the application window.
    #
    # @return Window height in pixels.
    def get_height(self):
        return self.window_height


##
# @brief Main entry point for the application.
#
# Creates and runs the main application loop.
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
