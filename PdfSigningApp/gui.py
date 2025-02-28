import customtkinter as ctk
import tkinter as tk
from usb_monitor import USBMonitor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def sign_btn_func():
    """Function called by Sign document button"""
    print("Sign PDF")
    # TODO: Button functionality


class PAdESSigningApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sign_button = None
        self.welcome_label = None
        self.title("PAdES Qualified Signing Tool")
        self.iconbitmap("icon.ico")

        # Window sizes
        window_width = 600
        window_height = 350

        # PC screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Positions to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.create_widgets()

        # USB Monitor
        self.usb_monitor = USBMonitor(self.update_ui)
        self.usb_monitor.start_monitoring()

    def create_widgets(self):
        self.welcome_label = ctk.CTkLabel(
            master=self,
            text=(
                "Welcome to the PAdES Signing Tool.\n"
                "Insert a USB drive with your private RSA key to begin."
            ),
            font=("Arial", 18)
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.sign_button = ctk.CTkButton(
            master=self,
            text="Sign Document",
            command=sign_btn_func
        )
        # Hidden by default
        self.sign_button.place_forget()

        # TODO: Another button to select pdf files

    def update_ui(self, key_found):
        """Switches UI views based on private key presence"""

        if key_found:
            # Hide the welcome label
            self.welcome_label.place_forget()
            # Show the sign button
            self.sign_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            # Show the welcome label
            self.welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            # Hide the sign button
            self.sign_button.place_forget()