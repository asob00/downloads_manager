from tkinter import *
from tkinter import filedialog
import os
import sys
import subprocess
from shutil import copyfile
from PIL import Image, ExifTags
import webbrowser


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
                                           title="Select destination directory:")
        if new_path:
            new_path = f"{new_path}/{self.file_basename}"
            os.rename(self.path, new_path)
            self.path = new_path

    def copy_file(self):
        """Opens path choosing window and copies file to selected location"""
        new_path = filedialog.askdirectory(initialdir=".",
                                           title="Select destination directory:")
        if new_path:
            new_path = f"{new_path}/{self.file_basename}"
            copyfile(self.path, new_path)

    def close_window(self):
        """Closes app"""
        self.root.destroy()
        sys.exit(0)


class ImageFile(MainWindow):
    """Class responsible for dealing with images inherits form MainWindow
    Parameters
    ----------
    path: same as in MainWindow

    Methods
    -------
    get_metadata()
        reads file metadata

    init_filename_label()
        adds information about image resolution in file frame

    init_action_frame()
        if possible adds show metadata button

    show_metadata()
        displays new window with written down all found metadata,
        if required GPS (GPSInfo, GPSLongitude and GPSLatitude)tags are found
        displays button which opens new tab in browser with location of image
        in Google Maps
    """

    def __init__(self, path):
        self.path = path
        self.metadata = {}
        self.get_metadata()
        super().__init__(self.path)

    def get_metadata(self):
        """Reads image metadata"""
        image = Image.open(self.path)
        exif = image.getexif()

        if not exif:
            return

        for tag, value in exif.items():
            if tag in ExifTags.TAGS:
                self.metadata[ExifTags.TAGS[tag]] = value

    def init_filename_label(self):
        """Additionally shows image resolution"""
        super().init_filename_label()
        if all(tag in self.metadata.keys()
               for tag in ('ExifImageHeight', 'ExifImageWidth')):

            size = f"{self.metadata['ExifImageWidth']}x" \
                   f"{self.metadata['ExifImageHeight']}"

        else:
            size = 'unknown'

        size_label = Label(self.filename_label_frame,
                           text=f"Size: {size}",
                           font="bold")
        size_label.pack(anchor="w")

    def init_action_frame(self):
        """Adds possibility to show additional metadata
        if possible
        """
        super().init_action_frame()

        if not self.metadata:
            return
        metadata_button = Button(self.action_frame,
                                 text="Show metadata",
                                 font="bold",
                                 command=self.show_metadata)
        metadata_button.grid(row=self.last_in_grid, column=0, sticky="nsew")
        self.last_in_grid += 1

    def show_metadata(self):
        metadata_window = Toplevel()
        metadata_window.title("Metadata")

        if not self.metadata:
            return

        if 'GPSInfo' in self.metadata \
                and all(el in self.metadata['GPSInfo'].keys() for el in (2, 4)):
            gps_data = self.metadata['GPSInfo']
            latitude = gps_data[2]
            longitude = gps_data[4]
            latitude = float(latitude[0] + latitude[1] / 60 + latitude[2] / 3600)
            longitude = float(longitude[0] + longitude[1] / 60 + longitude[2] / 3600)
            google_maps_url = f"https://www.google.pl/maps/place/{latitude},{longitude}"
            Button(metadata_window,
                   text="Find image location in Google Maps",
                   font="bold",
                   bg="#34495e",
                   bd=3,
                   relief="raised",
                   command=lambda: webbrowser.open_new_tab(google_maps_url)
                   ).pack(fill=BOTH, ipady=10)
            del self.metadata['GPSInfo']

        for key, val in self.metadata.items():
            if isinstance(val, bytes):
                val = val.decode('UTF-8')

            Label(metadata_window, text=f"{key}: {val}", font="bold").pack(ipadx=10, anchor=W)


root = ImageFile("/home/adam/Pulpit/3.jpg")
root.root.mainloop()
