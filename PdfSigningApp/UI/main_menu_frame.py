import customtkinter as ctk


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        """
        Sets up buttons to allow user switching between frames
        Available buttons:
        - Sign
        - Verify
        - KeyGen
        """
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
                             height=(controller.get_height() / 5), width=controller.get_width(), )

        empty.pack(pady=5)

        # Empty label at bottom to change bg color
        empty1 = ctk.CTkLabel(self, text="", fg_color="transparent",
                             height=(controller.get_height() / 5), width=controller.get_width(), )
        empty1.pack()
