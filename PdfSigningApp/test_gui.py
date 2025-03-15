import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from usb_monitor import USBMonitor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initial settings
        self.iconbitmap("icon.ico")
        self.title("Digital signature tool")
        self.window_width = 800
        self.window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Positions for centering window
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (MainMenu, SignFrame, VerifyFrame, GenerateKeysFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # puts pages in the same location
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Shows a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def get_width(self):
        return self.window_width

    def get_height(self):
        return self.window_height


# Main Menu
class MainMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        widgets_num = 5
        label = ctk.CTkLabel(self, text="Digital Signature Tool", fg_color="transparent",
                             height=(controller.get_height() / widgets_num), width=controller.get_width(),
                             font=("Arial", 30, "bold"))
        label.pack(pady=5)

        sign_button = ctk.CTkButton(self, text="Sign PDF", font=("Arial", 25, "bold"),
                                    height=(controller.get_height() / widgets_num),
                                    width=(controller.get_width() / 3),
                                    command=lambda: controller.show_frame("SignFrame"))
        sign_button.pack(pady=5)

        verify_button = ctk.CTkButton(self, text="Verify Signature", font=("Arial", 25, "bold"),
                                      height=(controller.get_height() / widgets_num),
                                      width=(controller.get_width() / 3),
                                      command=lambda: controller.show_frame("VerifyFrame"))
        verify_button.pack(pady=5)

        generate_button = ctk.CTkButton(self, text="Generate Key Pair", font=("Arial", 25, "bold"),
                                        height=(controller.get_height() / widgets_num),
                                        width=(controller.get_width() / 3),
                                        command=lambda: controller.show_frame("GenerateKeysFrame"))
        generate_button.pack(pady=5)

        # Empty label at bottom to change bg color
        empty = ctk.CTkLabel(self, text="", fg_color="transparent",
                             height=(controller.get_height() / widgets_num), width=controller.get_width(),)
        empty.pack()


class SignFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Sign pdf", font=("Arial", 25))
        label.pack(pady=40)

        back_button = ctk.CTkButton(self, text="Back to Menu", font=("Arial", 25),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=20)


class VerifyFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Verify a Signature", font=("Arial", 25))
        label.pack(pady=40)

        back_button = ctk.CTkButton(self, text="Back to Menu", font=("Arial", 25),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=20)


class GenerateKeysFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = ctk.CTkLabel(self, text="Generate Keys", font=("Arial", 25))
        label.pack(pady=40)

        back_button = ctk.CTkButton(self, text="Back to Menu", font=("Arial", 25),
                                    command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(pady=20)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
