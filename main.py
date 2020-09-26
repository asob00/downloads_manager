from tkinter import *
from tkinter import filedialog
import os
import sys
import subprocess
from shutil import copyfile
from PIL import Image, ExifTags


class MainWindow:

    def __init__(self, path):
        self.path = path
        self.root = Tk()
        self.filename_label_frame = LabelFrame(self.root, text="File:")
        self.action_frame = LabelFrame(self.root, text="Action:")
        self.rename_entry = None
        self.rename_canvas = Canvas(self.action_frame)
        self.rename_button = Button(self.rename_canvas, text="Rename file", font="bold", command=self.rename_file)
        self.configure_root(300, 600)
        self.init_filename_label()
        self.init_action_frame()

    @property
    def file_basename(self):
        return os.path.basename(f"{self.path}")

    def configure_root(self, width, height, bg_color="black"):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(bg=bg_color)
        self.root.title("Downloads manager")
        self.root.minsize(width, height)
        self.root.geometry(f"{width}x{height}+500+200")

    def init_filename_label(self):
        self.filename_label_frame.grid(row=0, column=0, sticky="nsew")
        file_name_label = Label(self.filename_label_frame, text=f"Name: {self.file_basename}", font="bold")
        file_path_label = Label(self.filename_label_frame, text=f"Path: {self.path}", font="bold")
        file_name_label.pack(anchor="w")
        file_path_label.pack(anchor="w")

    def init_action_frame(self):
        self.action_frame.grid(row=1, column=0, sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        open_button = Button(self.action_frame, text="Open file", font="bold", command=self.open_file)
        copy_button = Button(self.action_frame, text="Copy file", font="bold", command=self.copy_file)
        move_button = Button(self.action_frame, text="Move file", font="bold", command=self.move_file)
        do_nothing_button = Button(self.action_frame, text="Quit", font="bold", command=self.close_window)
        open_button.grid(row=0, column=0, sticky="nsew")
        self.rename_canvas.grid(row=1, column=0, sticky="nsew")
        self.rename_button.pack(fill=X)
        copy_button.grid(row=2, column=0, sticky="nsew")
        move_button.grid(row=3, column=0, sticky="nsew")
        do_nothing_button.grid(row=4, column=0, sticky="nsew")

    def open_file(self):
        if sys.platform == 'win32':
            os.startfile(self.path)
        elif sys.platform == 'darwin':
            subprocess.call(['open', self.path])
        else:
            subprocess.call(['xdg-open', self.path])

    def rename_file(self):
        for button in self.rename_canvas.winfo_children():
            button.destroy()
        self.rename_entry = Entry(self.rename_canvas)
        self.rename_entry.pack(fill=BOTH)
        self.rename_entry.bind('<Return>', lambda x: self.set_new_name())

    def set_new_name(self):
        filepath = os.path.dirname(self.path)
        new_name = self.rename_entry.get()
        new_path = filepath + "/" + new_name
        os.rename(self.path, new_path)
        self.path = new_path
        self.rename_canvas.winfo_children()[0].destroy()
        self.rename_button = Button(self.rename_canvas, text="Rename file", font="bold", command=self.rename_file)
        self.rename_button.pack(fill=X)

    def move_file(self):
        new_path = filedialog.askdirectory(initialdir=".",
                                              title="Select destination directory:")
        if new_path:
            new_path = new_path + f"/{self.file_basename}"
            os.rename(self.path, new_path)
            self.path = new_path

    def copy_file(self):
        new_path = filedialog.askdirectory(initialdir=".",
                                           title="Select destination directory:")
        if new_path:
            new_path = new_path + f"/{self.file_basename}"
            copyfile(self.path, new_path)

    def close_window(self):
        self.root.destroy()


class ImageFile(MainWindow):
    def __init__(self, path):
        self.metadata = {}
        self.path = path
        self.get_metadata()
        super().__init__(path)

    def get_metadata(self):
        image = Image.open(self.path)
        exif = image.getexif()
        print(ExifTags.TAGS)
        if exif:
            for tag, value in exif.items():
                if tag in ExifTags.TAGS:
                    self.metadata[ExifTags.TAGS[tag]] = value

    def init_filename_label(self):
        super().init_filename_label()
        if 'ExifImageWidth' in self.metadata.keys() \
                and 'ExifImageHeight' in self.metadata.keys():
            size = f"{self.metadata['ExifImageWidth']}x" \
                   f"{self.metadata['ExifImageHeight']}"
        else:
            size = 'unknown'
        size_label = Label(self.filename_label_frame,
                           text=f"Size: {size}",
                           font="bold")
        size_label.pack(anchor="w")


root = ImageFile("/home/adam/Pulpit/1.jpg")
root.root.mainloop()

