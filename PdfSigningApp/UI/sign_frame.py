import customtkinter as ctk


class SignFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Sign pdf", font=("Arial", 25))
        label.pack(pady=40)

        back_button = ctk.CTkButton(self, text="Back to Menu", font=("Arial", 25),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=20)
