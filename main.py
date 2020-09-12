from tkinter import *
import os


class MainClass:

    def __init__(self, path):
        self.path = path
        self.root = Tk()
        self.filename_label = LabelFrame(self.root, text="File:")
        self.action_frame = LabelFrame(self.root, text="action")
        self.configure_root(300, 600)
        self.init_filename_label()

    @property
    def file_name(self):
        return os.path.basename(f"{self.path}")

    @file_name.setter
    def file_name(self, path):
        self.path = path

    def configure_root(self, width, height, bg_color="black"):
        self.root.configure(bg=bg_color)
        self.root.minsize(width, height)

    def init_filename_label(self):
        self.filename_label.place(relx=0.1, y=10, relwidth=0.8)
        file_name_label = Label(self.filename_label, text=f"Name: {self.file_name}")
        file_name_label.pack()

root = MainClass("/home/adam/Pulpit/1")
root.root.mainloop()