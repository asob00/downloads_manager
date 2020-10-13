from tkinter import *
from PIL import Image, ExifTags
import webbrowser
import MainWindow


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
