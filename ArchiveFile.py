from tkinter import *
from tkinter import filedialog
import sys
import shutil
import MainWindow


class ArchiveFile(MainWindow):
    def __init__(self, path):
        super().__init__(path)

    def init_action_frame(self):
        super().init_action_frame()
        Button(self.action_frame,
               text="Unpack archive",
               font="bold",
               command=self.extract_zip_file
               ).grid(row=self.last_in_grid,
                      column=0, sticky="nsew")
        self.last_in_grid += 1

    def extract_zip_file(self):
        new_path = filedialog.askdirectory(initialdir=".",
                                           title=self.dst_window_title)
        try:
            shutil.unpack_archive(self.path, new_path)
            print("Done")
        except shutil.ReadError:
            sys.stderr.write('Unknown file format.')
