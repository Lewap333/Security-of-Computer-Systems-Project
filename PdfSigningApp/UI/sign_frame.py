##
# @file sign_frame.py
# @brief GUI frame to select a PDF file and sign it using a private RSA key on USB.
#
# The frame provides UI elements to pick a PDF file, display status,
# monitor USB insertion/removal for private key presence,
# and sign the PDF after password input.

import os
import customtkinter as ctk
from tkinter import filedialog as fd
from sign import sign_pdf
from UI.password_dialog import PasswordDialog
from usb_monitor import USBMonitor
from tkinter import messagebox

##
# @brief Frame to handle PDF signing functionality.
#
# Allows user to select PDF, detects private key on USB drives,
# requests password, signs the PDF, and shows relevant UI updates.
class SignFrame(ctk.CTkFrame):
    ##
    # @brief Initializes the signing frame UI and USB monitoring.
    #
    # @param parent Parent widget.
    # @param controller Controller providing window dimensions and frame switching.
    def __init__(self, parent, controller):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Sign PDF document",
                             fg_color="transparent",
                             height=(controller.get_height() / 5),
                             width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        title.pack(pady=5)

        self.info = ctk.CTkLabel(self, text="Insert a USB drive with your private RSA key to begin",
                                 fg_color="transparent",
                                 height=(controller.get_height() / 7),
                                 width=controller.get_width(),
                                 font=("Arial", 25))
        self.info.pack(pady=5)

        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack()

        self.selected_file_label = ctk.CTkLabel(self.file_frame, text="No file selected",
                                                fg_color="transparent",
                                                height=(controller.get_height() / 8),
                                                width=(controller.get_width() / 4),
                                                font=("Arial", 25))
        self.selected_file_label.pack(padx=10, pady=5, side="right")

        self.select_file_button = ctk.CTkButton(self.file_frame, text="Select file",
                                                font=("Arial", 25),
                                                height=(controller.get_height() / 8),
                                                width=(controller.get_width() / 4),
                                                command=self.choose_pdf)
        self.select_file_button.pack(padx=10, pady=5, side="left")

        self.sign_button = ctk.CTkButton(self, text="Sign",
                                         font=("Arial", 25),
                                         height=(controller.get_height() / 8),
                                         width=(controller.get_width() / 4),
                                         command=self.sign_btn)
        self.sign_button.pack(pady=5)

        self.empty = ctk.CTkLabel(self, text="",
                                  fg_color="transparent",
                                  height=(controller.get_height() / 7),
                                  width=controller.get_width(),
                                  font=("Arial", 25))
        self.empty.pack(pady=5)

        back_button = ctk.CTkButton(self, text="Back to Menu",
                                    font=("Arial", 25),
                                    height=(controller.get_height() / 8),
                                    width=(controller.get_width() / 4),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        self.usb_monitor = USBMonitor(self.update_ui)
        self.usb_monitor.start_monitoring()
        self.usb_monitor.initial_key_check()

        self.pdf_to_sign = None

    ##
    # @brief Opens file dialog for user to select a PDF file.
    # Updates label with selected file name.
    def choose_pdf(self):
        self.pdf_to_sign = fd.askopenfilename(title="Choose PDF file", filetypes=[("PDF files", "*.pdf")])

        label_text = self.pdf_to_sign
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_file_label.configure(text=os.path.basename(label_text))

    ##
    # @brief Handles Sign button click:
    # - disables buttons
    # - prompts for private key password
    # - calls sign_pdf function
    # - shows success or error message
    # - re-enables buttons
    def sign_btn(self):
        self.select_file_button.configure(state="disabled")
        self.sign_button.configure(state="disabled")
        if self.pdf_to_sign:
            dialog = PasswordDialog(self, "Enter Private Key password")
            self.wait_window(dialog)
            if dialog.result:
                if sign_pdf(self.pdf_to_sign, self.usb_monitor.get_key_file_path(), dialog.result):
                    messagebox.showinfo(title="Signing complete", message="PDF Signed Successfully!")
                else:
                    messagebox.showerror(title="Wrong password", message="Incorrect private key password!")

        self.select_file_button.configure(state="normal")
        self.sign_button.configure(state="normal")

    ##
    # @brief Updates UI to indicate private key found on USB drive.
    def view_with_private_key(self):
        key = self.usb_monitor.get_key_file_path()

        label_text = key
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]

        self.info.configure(text=f"Private key found: {label_text}")
        self.select_file_button.configure(state="normal")
        self.sign_button.configure(state="normal")

    ##
    # @brief Updates UI to indicate no private key found and disables buttons.
    def view_without_private_key(self):
        self.info.configure(text="Insert a USB drive with your private RSA key")
        self.select_file_button.configure(state="disabled")
        self.sign_button.configure(state="disabled")

    ##
    # @brief Callback for USBMonitor to update UI when key presence changes.
    # @param key_found True if private key detected on USB, False otherwise.
    def update_ui(self, key_found):
        if key_found:
            self.view_with_private_key()
        else:
            self.view_without_private_key()
