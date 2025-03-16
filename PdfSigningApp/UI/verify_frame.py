import customtkinter as ctk
import os
from tkinter import filedialog as fd, messagebox
from verify import verify_pdf

class VerifyFrame(ctk.CTkFrame):
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

    def choose_pdf(self):
        # Choose .pdf file
        self.pdf_to_verify = fd.askopenfilename(title="Choose PDF file", filetypes=[("PDF files", "*.pdf")])

        label_text = os.path.basename(self.pdf_to_verify)
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_file_label.configure(text=os.path.basename(label_text))

        # self.pdf_icon = Image.open("pdf_icon.png")
        # self.pdf_icon = self.pdf_icon.resize((100, 100))
        # self.pdf_icon_tk = ImageTk.PhotoImage(self.pdf_icon)
        #
        # self.label_icon = tk.Label(self, image=self.pdf_icon_tk, bg="white")
        # self.label_icon.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

    def choose_pem(self):
        self.public_key_path = fd.askopenfilename(title="Choose key file", filetypes=[("pem files", "*.pem")])

        label_text = os.path.basename(self.public_key_path)
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_key_label.configure(text=os.path.basename(label_text))

    def verify_btn(self):
        if self.pdf_to_verify and self.public_key_path:
            if verify_pdf(self.pdf_to_verify, self.public_key_path):
                messagebox.showinfo(title="Signature verification", message="Signature is valid! File is authentic! ✔")
            else:
                messagebox.showerror(title="Signature verification", message="Invalid signature! File was modified! ❌")

