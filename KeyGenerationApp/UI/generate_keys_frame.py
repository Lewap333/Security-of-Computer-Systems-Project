##
# @file generate_keys_frame.py
# @brief GUI frame for generating RSA key pairs and saving them to disk (public) and USB (private).
#
# Uses customtkinter for UI rendering. Public key is stored in selected folder;
# private key is saved to USB drive after password-based encryption. USB plug detection included.

import customtkinter as ctk
from tkinter import filedialog as fd
from UI.password_dialog import PasswordDialog
import threading
import time
import utils
from usb_monitor import USBMonitor

##
# @class GenerateKeysFrame
# @brief A customtkinter frame for RSA key pair generation with USB support.
#
# Provides UI for:
# - selecting public key destination
# - monitoring USB plug/unplug to store private key
# - entering password to encrypt private key
class GenerateKeysFrame(ctk.CTkFrame):
    ##
    # @brief Constructor. Initializes UI layout, USB monitor, and labels.
    # @param parent The parent frame.
    # @param controller The main controller to access app dimensions and state transitions.
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.dir_path = None
        title = ctk.CTkLabel(self, text="RSA Key Generation",
                             fg_color="transparent",
                             height=(controller.get_height() / 5),
                             width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        title.pack(pady=5)

        self.private_key_label = ctk.CTkLabel(self, text="Insert USB drive for your private key",
                                              fg_color="transparent",
                                              height=(controller.get_height() / 7),
                                              width=controller.get_width(),
                                              font=("Arial", 25))

        self.private_key_label.pack(pady=5)

        self.pub_label = ctk.CTkLabel(self, text="Select folder for public key",
                                      fg_color="transparent",
                                      height=(controller.get_height() / 7),
                                      width=controller.get_width(),
                                      font=("Arial", 25))

        self.pub_label.pack(pady=5)

        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.file_frame.pack()

        self.selected_dir_label = ctk.CTkLabel(self.file_frame, text="Folder not selected",
                                               fg_color="transparent",
                                               height=(controller.get_height() / 8),
                                               width=(controller.get_width() / 4),
                                               font=("Arial", 25))
        self.selected_dir_label.pack(padx=10, pady=5, side="right")

        self.select_dir_button = ctk.CTkButton(self.file_frame, text="Select folder",
                                               font=("Arial", 25),
                                               height=(controller.get_height() / 8),
                                               width=(controller.get_width() / 4),
                                               command=self.select_dir_btn)
        self.select_dir_button.pack(padx=10, pady=5, side="left")

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
        self.usb_monitor = USBMonitor(self.update_ui)
        self.usb_monitor.start_monitoring()
        self.usb_monitor.initial_drive_check()

    ##
    # @brief Opens a dialog to select folder where the public key will be stored.
    def select_dir_btn(self):
        dir_path = fd.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            if len(dir_path) > 36:
                dir_text = '...%s' % dir_path[-33:]
            else:
                dir_text = dir_path
            self.selected_dir_label.configure(text=dir_text)

    ##
    # @brief Starts password dialog and then launches key generation in a separate thread.
    def gen_keys_btn(self):
        self.generate_button.configure(state="disabled")
        self.select_dir_button.configure(state="disabled")
        if self.dir_path:
            dialog = PasswordDialog(self, "Encrypt Private Key")
            self.wait_window(dialog)
            if dialog.result:
                self.running_animation = True
                self.gen_animation()
                threading.Thread(target=self.gen_thread, args=(dialog.result,), daemon=True).start()
                return
        self.generate_button.configure(state="normal")
        self.select_dir_button.configure(state="normal")

    ##
    # @brief Updates the UI text label with a dot animation while keys are generating.
    def gen_animation(self):
        if self.running_animation:
            dots = ["", ".", "..", "..."]
            current_text = "Generating key pair" + dots[int(time.time() % 4)]
            self.private_key_label.configure(text=current_text)
            self.after(500, self.gen_animation)

    ##
    # @brief Worker thread that generates RSA key pair using `utils.generate_key_pair`.
    # @param pwd The password used to encrypt the private key.
    def gen_thread(self, pwd):
        utils.generate_key_pair(self.dir_path, self.usb_monitor.get_drive(), pwd)
        self.running_animation = False
        self.private_key_label.configure(text="Key pair generated!")
        self.generate_button.configure(state="normal")
        self.select_dir_button.configure(state="normal")

    ##
    # @brief Callback for USB monitor to update interface based on drive availability.
    # @param usb_found Boolean flag whether USB is connected.
    def update_ui(self, usb_found):
        if usb_found:
            self.view_with_USB()
        else:
            self.view_without_USB()

    ##
    # @brief Sets UI state when USB is found.
    def view_with_USB(self):
        self.private_key_label.configure(text="USB drive found, " + self.usb_monitor.get_drive() + " !")
        if self.dir_path:
            self.generate_button.configure(state="disabled")
        else:
            self.generate_button.configure(state="normal")
        self.select_dir_button.configure(state="normal")

    ##
    # @brief Sets UI state when USB is not detected.
    def view_without_USB(self):
        self.private_key_label.configure(text="Insert USB drive for your private key")
        self.generate_button.configure(state="disabled")
        self.select_dir_button.configure(state="disabled")
