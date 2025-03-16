import customtkinter as ctk
from tkinter import filedialog as fd
from UI.password_dialog import PasswordDialog
import os
import threading
import time
import utils


class GenerateKeysFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        """
        Sets up buttons for:
        - selecting destination folder for key pair
        - generating key pair if folder is specified
        - going back to main menu
        Before generation user is asked for password.
        Generating keys is done in a separate thread.
        """
        super().__init__(parent)

        self.dir_path = None

        title = ctk.CTkLabel(self, text="RSA Key Generation",
                             fg_color="transparent",
                             height=(controller.get_height() / 5),
                             width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        title.pack(pady=5)

        self.dir_label = ctk.CTkLabel(self, text="Choose a folder to store your key pair",
                                      fg_color="transparent",
                                      height=(controller.get_height() / 7),
                                      width=controller.get_width(),
                                      font=("Arial", 25))

        self.dir_label.pack(pady=5)

        self.dir_select_button = ctk.CTkButton(self, text="Select folder",
                                               font=("Arial", 25),
                                               height=(controller.get_height() / 8),
                                               width=(controller.get_width() / 4),
                                               command=self.select_dir_btn)
        self.dir_select_button.pack(pady=5)

        self.generate_button = ctk.CTkButton(self, text="Generate Keys",
                                             font=("Arial", 25),
                                             height=(controller.get_height() / 8),
                                             width=(controller.get_width() / 4),
                                             command=self.gen_keys_btn)
        self.generate_button.pack(pady=5)

        self.empty = ctk.CTkLabel(self, text="",
                                  fg_color="transparent",
                                  height=(controller.get_height() / 7),
                                  width=controller.get_width(),
                                  font=("Arial", 25))
        self.empty.pack(pady=5)

        self.running_animation = False

        back_button = ctk.CTkButton(self, text="Back to Menu",
                                    font=("Arial", 25),
                                    height=(controller.get_height() / 8),
                                    width=(controller.get_width() / 4),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=5)

    def select_dir_btn(self):
        """
        Opens directory selection dialog
        result is saved at dir_path.
        Updates label with currently selected directory
        """
        dir_path = fd.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            dir_text = os.path.basename(os.path.normpath(dir_path))
            self.dir_label.configure(text="Destination folder: " + dir_text)

    def gen_keys_btn(self):
        """
        Runs key generation in separate thread.
        Buttons for key gen and dir select are disabled until generation finishes
        """
        self.generate_button.configure(state="disabled")
        self.dir_select_button.configure(state="disabled")
        if self.dir_path:
            dialog = PasswordDialog(self, "Encrypt Private Key")
            self.wait_window(dialog)
            if dialog.result:
                self.running_animation = True
                self.gen_animation()

                threading.Thread(target=self.gen_thread, args=(dialog.result,), daemon=True).start()
                return

        self.generate_button.configure(state="normal")
        self.dir_select_button.configure(state="normal")

    def gen_animation(self):
        """
        Dot animation to visualize key generation process
        """
        if self.running_animation:
            dots = ["", ".", "..", "..."]
            current_text = "Generating keys" + dots[int(time.time() % 4)]
            self.dir_label.configure(text=current_text)
            self.after(500, self.gen_animation)

    def gen_thread(self, pwd):
        """
        Thread function for key generation and updating label after its finished
        """
        utils.generate_key_pair(self.dir_path, pwd)
        dir_text = os.path.basename(os.path.normpath(self.dir_path))
        self.running_animation = False
        self.dir_label.configure(text="Key pair generated at: " + dir_text)
        self.generate_button.configure(state="normal")
        self.dir_select_button.configure(state="normal")
