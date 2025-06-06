##
# @file verify_frame.py
# @brief GUI frame to select a PDF and public key to verify the digital signature.
#
# Allows user to select a signed PDF file and a public key file,
# then verifies the signature and displays the result.

import customtkinter as ctk
import os
from tkinter import filedialog as fd, messagebox
from verify import verify_pdf

##
# @brief Frame to handle PDF signature verification functionality.
#
# Allows user to select PDF and public key files, then verify the signature.
class VerifyFrame(ctk.CTkFrame):
    ##
    # @brief Initializes the verify frame UI.
    #
    # @param parent Parent widget.
    # @param controller Controller with window dimensions and frame switching.
    def __init__(self, parent, controller):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="Verify signature",
                             fg_color="transparent",
                             height=(controller.get_height() / 5),
                             width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        title.pack(pady=5)

        self.info = ctk.CTkLabel(self, text="Select a PDF file and a public key to verify the signature.",
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

        self.key_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.key_frame.pack()

        self.selected_key_label = ctk.CTkLabel(self.key_frame, text="No key selected",
                                               fg_color="transparent",
                                               height=(controller.get_height() / 8),
                                               width=(controller.get_width() / 4),
                                               font=("Arial", 25))
        self.selected_key_label.pack(padx=10, pady=5, side="right")

        self.select_key_button = ctk.CTkButton(self.key_frame, text="Select key",
                                               font=("Arial", 25),
                                               height=(controller.get_height() / 8),
                                               width=(controller.get_width() / 4),
                                               command=self.choose_pem)
        self.select_key_button.pack(padx=10, pady=5, side="left")

        back_button = ctk.CTkButton(self, text="Verify",
                                    font=("Arial", 25),
                                    height=(controller.get_height() / 8),
                                    width=(controller.get_width() / 4),
                                    command=self.verify_btn)
        back_button.pack(pady=5)

        back_button = ctk.CTkButton(self, text="Back to Menu",
                                    font=("Arial", 25),
                                    height=(controller.get_height() / 8),
                                    width=(controller.get_width() / 4),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

        self.pdf_to_verify = None
        self.public_key_path = None

    ##
    # @brief Opens file dialog for user to select a PDF file to verify.
    def choose_pdf(self):
        self.pdf_to_verify = fd.askopenfilename(title="Choose PDF file", filetypes=[("PDF files", "*.pdf")])

        label_text = os.path.basename(self.pdf_to_verify)
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_file_label.configure(text=os.path.basename(label_text))

    ##
    # @brief Opens file dialog for user to select a PEM public key file.
    def choose_pem(self):
        self.public_key_path = fd.askopenfilename(title="Choose key file", filetypes=[("pem files", "*.pem")])

        label_text = os.path.basename(self.public_key_path)
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_key_label.configure(text=os.path.basename(label_text))

    ##
    # @brief Called when Verify button clicked.
    #
    # Checks if PDF and key are selected, calls verify_pdf,
    # then displays messagebox with verification result.
    def verify_btn(self):
        if self.pdf_to_verify and self.public_key_path:
            if verify_pdf(self.pdf_to_verify, self.public_key_path):
                messagebox.showinfo(title="Signature verification", message="Signature is valid! File is authentic! ✔")
            else:
                messagebox.showerror(title="Signature verification", message="Invalid signature! File was modified! ❌")
