##
# @file password_dialog.py
# @brief Dialog window to securely input a password with minimal length validation.
#
# Provides a modal dialog that requests the user to input a password of at least 4 characters.
# Shows an error message if the password is too short.
# The entered password is stored in the `result` attribute or None if cancelled.

import customtkinter as ctk
from tkinter import messagebox

##
# @brief Modal password input dialog.
#
# Opens a window centered on the screen with password entry field.
# Validates password length (minimum 4 characters).
# Stores the result in self.result.
class PasswordDialog(ctk.CTkToplevel):
    ##
    # @brief Initializes the password dialog window.
    #
    # @param parent Parent window for modality.
    # @param title Title of the dialog window.
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
    # If the password is too short, shows an error message.
    def confirm(self):
        password = self.entry.get()
        if len(password) >= self.min_length:
            self.result = password
            self.destroy()
        else:
            messagebox.showerror("Invalid Password", f"Password must be at least {self.min_length} characters long.")

    ##
    # @brief Cancels the dialog and sets result to None.
    def cancel(self):
        self.result = None
        self.destroy()
