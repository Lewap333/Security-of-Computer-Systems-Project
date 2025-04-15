import customtkinter as ctk
from UI.generate_keys_frame import GenerateKeysFrame

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
        # Centering window
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2

        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        self.frames["GenerateKeysFrame"] = GenerateKeysFrame(self.container, controller=self)
        self.frames["GenerateKeysFrame"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("GenerateKeysFrame")

    def show_frame(self, page_name):
        """Shows a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def get_width(self):
        return self.window_width

    def get_height(self):
        return self.window_height


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
