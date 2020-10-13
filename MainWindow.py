from tkinter import *
from tkinter import filedialog
import os
import sys
import subprocess
import shutil


class MainWindow:
    """Main class of application, responsible for generating simple view.
    Applies to every type of file, possible operations:
    - opening file with default system app
    - renaming file
    - moving file to different location
    - copying file
    - closing this app

    Attributes
    ----------
    :param path: path to used file
    :type path str

    Methods
    -------
    configure_root(width, height, bg_color="black")
        Sets default window parameters

    init_filename_label()
        Creates frame containing filename and file path

    init_action_frame()
        Creates frame containing buttons responsible for file operations

    add_quit_button()
        Adds quit button (as last button)

    open_file()
        Opens file with default system app

    rename_file()
        Renames file

    set_new_name()
        Used by rename file function

    move_file()
        Opens path choosing window and moves file to selected location

    copy_file()
        Opens path choosing window and copies file to selected location

    close_window()
        Closes app
    """

    def __init__(self, path):
        """
        Parameters
        ----------
        :param path: path to used file
        :type path: str
        """
        self.path = path
        self.root = Tk()
        self.filename_label_frame = LabelFrame(self.root,
                                               text="File:")
        self.action_frame = LabelFrame(self.root,
                                       text="Action:")
        self.rename_entry = None
        self.rename_canvas = Canvas(self.action_frame)
        self.rename_button = Button(self.rename_canvas,
                                    text="Rename file",
                                    font="bold",
                                    command=self.rename_file)
        self.last_in_grid = 4
        self.dst_window_title = "Select destination directory:"
        self.configure_root(300, 600)
        self.init_filename_label()
        self.init_action_frame()
        self.add_quit_button()

    @property
    def file_basename(self) -> str:
        """Returns basename of the file
        :return: basename of the file
        """
        return os.path.basename(f"{self.path}")

    def configure_root(self, width, height, bg_color="black"):
        """Configures main window

        Parameters
        ----------
        :param width: window minimal width
        :type width: int

        :param height: window minimal height
        :type height: int

        :param bg_color: main window background
        :type bg_color: str
        """
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(bg=bg_color)
        self.root.title("Downloads manager")
        self.root.minsize(width, height)
        self.root.geometry(f"{width}x{height}+500+200")

    def init_filename_label(self):
        """Creates frame containing filename and file path"""
        self.filename_label_frame.grid(row=0, column=0, sticky="nsew")
        file_name_label = Label(self.filename_label_frame,
                                text=f"Name: {self.file_basename}",
                                font="bold")
        file_path_label = Label(self.filename_label_frame,
                                text=f"Path: {self.path}",
                                font="bold")
        file_name_label.pack(anchor="w")
        file_path_label.pack(anchor="w")

    def init_action_frame(self):
        """Creates frame containing buttons responsible for file operations"""
        self.action_frame.grid(row=1, column=0, sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        open_button = Button(self.action_frame,
                             text="Open file",
                             font="bold",
                             command=self.open_file)
        copy_button = Button(self.action_frame,
                             text="Copy file",
                             font="bold",
                             command=self.copy_file)
        move_button = Button(self.action_frame,
                             text="Move file",
                             font="bold",
                             command=self.move_file)
        open_button.grid(row=0, column=0, sticky="nsew")
        self.rename_canvas.grid(row=1, column=0, sticky="nsew")
        self.rename_button.pack(fill=X)
        copy_button.grid(row=2, column=0, sticky="nsew")
        move_button.grid(row=3, column=0, sticky="nsew")

    def add_quit_button(self):
        """Initializes quit button"""
        do_nothing_button = Button(self.action_frame, text="Quit",
                                   font="bold",
                                   command=self.close_window)
        do_nothing_button.grid(row=self.last_in_grid,
                               column=0,
                               sticky="nsew")

    def open_file(self):
        """Opens file with default system app"""
        if sys.platform == 'win32':
            os.startfile(self.path)
        elif sys.platform == 'darwin':
            subprocess.call(['open', self.path])
        else:
            subprocess.call(['xdg-open', self.path])

    def rename_file(self):
        """Renames file"""
        for button in self.rename_canvas.winfo_children():
            button.destroy()
        self.rename_entry = Entry(self.rename_canvas)
        self.rename_entry.pack(fill=BOTH)
        self.rename_entry.bind('<Return>', lambda x: self.set_new_name())

    def set_new_name(self):
        """Sets app new name based on entry value"""
        filepath = os.path.dirname(self.path)
        new_name = self.rename_entry.get()
        new_path = f"{filepath}/{new_name}"
        os.rename(self.path, new_path)
        self.path = new_path
        self.rename_canvas.winfo_children()[0].destroy()
        self.rename_button = Button(self.rename_canvas,
                                    text="Rename file",
                                    font="bold",
                                    command=self.rename_file)
        self.rename_button.pack(fill=X)

    def move_file(self):
        """Opens path choosing window and moves file to selected location"""
        new_path = filedialog.askdirectory(initialdir=".",
                                           title=self.dst_window_title)
        if new_path:
            new_path = f"{new_path}/{self.file_basename}"
            shutil.move(self.path, new_path)
            self.path = new_path

    def copy_file(self):
        """Opens path choosing window and copies file to selected location"""
        new_path = filedialog.askdirectory(initialdir=".",
                                           title=self.dst_window_title)
        if new_path:
            new_path = f"{new_path}/{self.file_basename}"
            shutil.copy2(self.path, new_path)

    def close_window(self):
        """Closes app"""
        self.root.destroy()
        sys.exit(0)
