##
# @file password_dialog.py
# @brief Custom password input dialog for encrypting RSA private keys.
#
# A popup window using customtkinter that prompts the user to enter a password
# of at least a minimum required length (default: 4 characters).

import customtkinter as ctk
from tkinter import messagebox

##
# @class PasswordDialog
# @brief A modal dialog to securely enter a password.
#
# The dialog validates that the password meets a minimum length before returning it.
# The password is saved in the `result` attribute if confirmed.
class PasswordDialog(ctk.CTkToplevel):
    ##
    # @brief Constructor for the password input dialog.
    # @param parent The parent tkinter widget.
    # @param title The title of the dialog window.
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.window_width = 320
        self.window_height = 180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.min_length = 4
        self.result = None

        self.label = ctk.CTkLabel(self, text=f"Enter Key Password:")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, show="*")
        self.entry.pack(pady=5, padx=10, fill="x")

        self.ok_button = ctk.CTkButton(self, text="OK", command=self.confirm)
        self.ok_button.pack(side="left", padx=5)

        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side="right", padx=5)

    ##
    # @brief Validates password length and stores result if valid.
    #
    # Displays error message if password is too short.
    def confirm(self):
        password = self.entry.get()
        if len(password) >= self.min_length:
            self.result = password
            self.destroy()
        else:
            messagebox.showerror("Invalid Password", f"Password must be at least {self.min_length} characters long.")

    ##
    # @brief Cancels the dialog and clears the result.
    def cancel(self):
        self.result = None
        self.destroy()
