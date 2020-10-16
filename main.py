from MainWindow import MainWindow
from ImageFile import ImageFile
from ArchiveFile import ArchiveFile
from VideoFile import VideoFile
import sys
import os
import re

path = sys.argv[1]
basename, extension = os.path.splitext(path)


def get_file_type(path):
    patterns = {'img': re.compile(r'.(png|jpg|jpeg|gif|tiff|raw|psd|eps|ai|indd)'),
                'archive': re.compile(r'.(tar|bz2|gz|7z|arc|ark|jar|rar|tar.gz|tgz|'
                                      r'tar.Z|tar.bz2|tbz2|tar.lz|tlz.tar.xz|txz|zip|zipx)'),
                'vid': re.compile(r'.(mkv|avi|mp4)')
                }

    for key, pattern in patterns.items():
        if pattern.search(path) and key == 'img':
            return ImageFile(path)
        elif pattern.search(path) and key == 'archive':
            return ArchiveFile(path)
        elif pattern.search(path) and key == 'vid':
            return VideoFile(path)
        else:
            return MainWindow(path)


root = get_file_type(path)
root.root.mainloop()
