# Image manipulation imports
from io import BytesIO

import PIL
import PIL.ImageTk
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.easymp4 import EasyMP4, EasyMP4KeyError

# Change import name for code clarity
from mutagen.flac import FLAC
from mutagen.flac import Picture as FlacPicture
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3


def initialize_metadata_Nb_Page(self, master):
    """Calls to draw the matadata widgets"""
    self.nb_metadata_frame = ttk.Frame(master)
    self.nb_metadata_frame.grid(sticky="nswe")
    self.nb_metadata_frame.columnconfigure(0, weight=1)
    self.nb_metadata_frame.columnconfigure(1, weight=1)
    self.nb_metadata_frame.rowconfigure(0, weight=1)

    # Entries with the Metadata
    self.metadata_list_entries = Metadata_ListEntries(self.nb_metadata_frame)
    # Attached Image
    self.metadata_img = Metadata_Img(self.nb_metadata_frame)
    # Apply buttons
    self.apply_changes = Apply_Changes(self.nb_metadata_frame)
