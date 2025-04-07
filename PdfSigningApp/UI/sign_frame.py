import os
import customtkinter as ctk
from tkinter import filedialog as fd
from sign import sign_pdf
from UI.password_dialog import PasswordDialog
from usb_monitor import USBMonitor
from tkinter import messagebox


class SignFrame(ctk.CTkFrame):
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

    def choose_pdf(self):
        # Choose .pdf file
        self.pdf_to_sign = fd.askopenfilename(title="Choose PDF file", filetypes=[("PDF files", "*.pdf")])

        label_text = self.pdf_to_sign
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]
        self.selected_file_label.configure(text=os.path.basename(label_text))

        # self.pdf_icon = Image.open("pdf_icon.png")
        # self.pdf_icon = self.pdf_icon.resize((100, 100))
        # self.pdf_icon_tk = ImageTk.PhotoImage(self.pdf_icon)
        #
        # self.label_icon = tk.Label(self, image=self.pdf_icon_tk, bg="white")
        # self.label_icon.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

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

    def view_with_private_key(self):
        key = self.usb_monitor.get_key_file_path()

        label_text = key
        if len(label_text) > 36:
            label_text = '...%s' % label_text[-33:]

        self.info.configure(text=f"Private key found: {label_text}")
        self.select_file_button.configure(state="normal")
        self.sign_button.configure(state="normal")

    def view_without_private_key(self):
        self.info.configure(text="Insert a USB drive with your private RSA key")
        self.select_file_button.configure(state="disabled")
        self.sign_button.configure(state="disabled")

    def update_ui(self, key_found):
        if key_found:
            self.view_with_private_key()
        else:
            self.view_without_private_key()
