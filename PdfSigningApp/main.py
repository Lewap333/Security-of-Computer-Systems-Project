##
# @file main.py
# @brief Main GUI application for signing and verifying PDF documents.
#
# Creates a graphical interface using the customtkinter library,
# allowing users to navigate between the main menu, signing, and verification screens.

import customtkinter as ctk
from UI.main_menu_frame import MainMenu
from UI.sign_frame import SignFrame
from UI.verify_frame import VerifyFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

##
# @class MainApp
# @brief Main GUI application class inheriting from CTk.
#
# Initializes and manages all application frames (menu, signing, verification).
class MainApp(ctk.CTk):
    ##
    # @brief Constructor for MainApp.
    #
    # Sets appearance, window size, and initializes all frames.
    def __init__(self):
        super().__init__()

        # Initial settings
        self.iconbitmap("icon.ico")
        self.title("Digital signature tool")
        self.window_width = 800
        self.window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Center the window
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize and place frames
        for F in (MainMenu, SignFrame, VerifyFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    ##
    # @brief Switches view to a specified frame.
    # @param page_name Name of the frame class to display.
    def show_frame(self, page_name):
        """Shows a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    ##
    # @brief Returns window width.
    # @return Window width as integer.
    def get_width(self):
        return self.window_width

    ##
    # @brief Returns window height.
    # @return Window height as integer.
    def get_height(self):
        return self.window_height


##
# @brief Application entry point.
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
