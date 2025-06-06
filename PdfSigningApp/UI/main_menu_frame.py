##
# @file main_menu_frame.py
# @brief Defines the main menu GUI for switching between application features.
#
# Provides the main interface allowing the user to navigate to different sections
# of the PDF signature application: signing, verification, and key generation.

import customtkinter as ctk

##
# @brief Main menu GUI frame for navigation between signing, verifying, and key generation.
#
# Displays buttons that allow the user to switch between:
# - Sign PDF
# - Verify Signature
# - (Reserved space for KeyGen, not implemented in this frame)
#
# @param parent The parent container widget.
# @param controller The main application controller used to change frames.
class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Digital Signature Tool", fg_color="transparent",
                             height=(controller.get_height() / 5), width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        label.pack(pady=5)

        sign_button = ctk.CTkButton(self, text="Sign PDF", font=("Arial", 25, "bold"),
                                    height=(controller.get_height() / 5),
                                    width=(controller.get_width() / 3),
                                    command=lambda: controller.show_frame("SignFrame"))
        sign_button.pack(pady=5)

        verify_button = ctk.CTkButton(self, text="Verify Signature", font=("Arial", 25, "bold"),
                                      height=(controller.get_height() / 5),
                                      width=(controller.get_width() / 3),
                                      command=lambda: controller.show_frame("VerifyFrame"))
        verify_button.pack(pady=5)

        # Empty label at bottom to change bg color
        empty = ctk.CTkLabel(self, text="", fg_color="transparent",
                             height=(controller.get_height() / 5), width=controller.get_width())
        empty.pack(pady=5)

        empty1 = ctk.CTkLabel(self, text="", fg_color="transparent",
                              height=(controller.get_height() / 5), width=controller.get_width())
        empty1.pack()
