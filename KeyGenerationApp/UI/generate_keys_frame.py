import customtkinter as ctk
from tkinter import filedialog as fd
from UI.password_dialog import PasswordDialog
import threading
import time
import utils
from usb_monitor import USBMonitor


class GenerateKeysFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        """
        Sets up buttons for:
        - selecting destination folder for public key
        - generating key pair if folder is specified
        - going back to main menu
        Before generation of private key user is asked for password.
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


    def select_dir_btn(self):
        """
        Opens directory selection dialog
        result is saved at dir_path.
        Updates label with currently selected directory
        """
        dir_path = fd.askdirectory()
        if dir_path:
            self.dir_path = dir_path
            if len(dir_path) > 36:
                dir_text = '...%s' % dir_path[-33:]
            self.selected_dir_label.configure(dir_path)

    def gen_keys_btn(self):
        """
        Runs key generation in separate thread.
        Buttons for key gen and dir select are disabled until generation finishes
        """
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

    def gen_animation(self):
        """
        Dot animation to visualize key generation process
        """
        if self.running_animation:
            dots = ["", ".", "..", "..."]
            current_text = "Generating key pair" + dots[int(time.time() % 4)]
            self.private_key_label.configure(text=current_text)
            self.after(500, self.gen_animation)

    def gen_thread(self, pwd):
        """
        Thread function for key generation and updating label after its finished
        """
        utils.generate_key_pair(self.dir_path,self.usb_monitor.get_drive(), pwd)

        self.running_animation = False
        self.private_key_label.configure(text="Key pair generated!")
        self.generate_button.configure(state="normal")
        self.select_dir_button.configure(state="normal")

    def update_ui(self, usb_found):
        if usb_found:
            self.view_with_USB()
        else:
            self.view_without_USB()


    def view_with_USB(self):
        self.private_key_label.configure(text="USB drive found, " + self.usb_monitor.get_drive() + " !")
        if self.dir_path:
            self.generate_button.configure(state="disabled")
        else:
            self.generate_button.configure(state="normal")
        self.select_dir_button.configure(state="normal")

    def view_without_USB(self):
        self.private_key_label.configure(text="Insert USB drive for your private key")
        self.generate_button.configure(state="disabled")
        self.select_dir_button.configure(state="disabled")