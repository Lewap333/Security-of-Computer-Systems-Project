import customtkinter as ctk
from tkinter import messagebox


class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, parent, title):
        """
        Password dialog that accepts pass at least 4 characters long.
        Shorter password gives error messagebox.
        Password is stored in 'result' variable
        result = None if dialog not completed properly
        """
        super().__init__(parent)
        self.title(title)
        self.window_width = 320
        self.window_height = 180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Centering the window
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

    def confirm(self):
        password = self.entry.get()
        if len(password) >= self.min_length:
            self.result = password
            self.destroy()
        else:
            messagebox.showerror("Invalid Password", f"Password must be at least {self.min_length} characters long.")

    def cancel(self):
        self.result = None
        self.destroy()
