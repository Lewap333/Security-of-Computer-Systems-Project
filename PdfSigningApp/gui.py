import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import pdf_sign as ps
from usb_monitor import USBMonitor
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PAdESSigningApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choose_file_button = None
        self.sign_button = None
        self.welcome_label = None
        self.title("PAdES Qualified Signing Tool")
        self.iconbitmap("icon.ico")

        self.pdf_icon = None
        self.pdf_icon_tk = None
        self.label_icon = None

        self.pdf_to_sign = None


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
            command=self.sign_btn_func
        )
        # Hidden by default
        self.sign_button.place_forget()

        self.choose_file_button = ctk.CTkButton(
            master=self,
            text="Choose .pdf file",
            command=self.choose_pdf_func
        )
        # Hidden by default
        self.choose_file_button.place_forget()

    def update_ui(self, key_found):
        """Switches UI views based on private key presence"""

        if key_found:
            # Hide the welcome label
            self.welcome_label.place_forget()
            # Show the sign button
            self.sign_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            self.choose_file_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        else:
            # Show the welcome label
            self.welcome_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            # Hide the sign button
            self.sign_button.place_forget()
            self.choose_file_button.place_forget()

    def sign_btn_func(self):
        """Function called by Sign document button"""
        if self.pdf_to_sign is None:
            tk.messagebox.showinfo(title="PDF file not selected", message="Choose a .pdf file to sign")
            return

        # TODO: Button functionality
        print("Sign PDF")
        ps.sign_pdf(self.pdf_to_sign)

    def choose_pdf_func(self):
        # Choose .pdf file
        self.pdf_to_sign = fd.askopenfilename(title="Wybierz plik PDF", filetypes=[("Pliki PDF", "*.pdf")])

        # self.pdf_icon = Image.open("pdf_icon.png")
        # self.pdf_icon = self.pdf_icon.resize((100, 100))
        # self.pdf_icon_tk = ImageTk.PhotoImage(self.pdf_icon)
        #
        # self.label_icon = tk.Label(self, image=self.pdf_icon_tk, bg="white")
        # self.label_icon.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

