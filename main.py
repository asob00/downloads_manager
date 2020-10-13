from MainWindow import MainWindow
from ImageFile import ImageFile
from ArchiveFile import ArchiveFile
import sys

root = ImageFile(sys.argv[1])
root.root.mainloop()
