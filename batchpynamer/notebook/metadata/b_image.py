import tkinter as tk

# Image manipulation imports
from io import BytesIO
from tkinter import ttk

import PIL
import PIL.ImageTk
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.easymp4 import EasyMP4, EasyMP4KeyError

# Change import name for code clarity
from mutagen.flac import FLAC
from mutagen.flac import Picture as FlacPicture
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

import batchpynamer as bpn
from batchpynamer.basewidgets import BaseWidget
from batchpynamer.notebook.metadata import utils


class MetadataImg(BaseWidget, ttk.Frame):
    """
    Draws the Metadata Image widget. Inside metadata notebook.
    It has:
        - An entry to write the path to the new image
        - A X button to empty the new image entry
        - A canvas to display the metadata image
    """

    def __init__(self):
        pass

    def tk_init(self, master, *args, **kwargs):
        super().__init__(master, column=1, row=0, sticky="ns")

        # Empty photo image to force the label to use pixel size
        self.photo_image = tk.PhotoImage()

        self.picture = None
        self.image_path = tk.StringVar()

        # Path to new image, entry
        self.image_path_entry = ttk.Entry(self, textvariable=self.image_path)
        self.image_path_entry.grid(column=0, row=0, sticky="ew")

        self.reset_path_button = ttk.Button(
            self, width=2, text="X", command=self.resetPath
        )
        self.reset_path_button.grid(column=1, row=0, sticky="w")

        # Image frame, Label
        self.img = tk.Label(
            self,
            relief="sunken",
            background="gray10",
            image=self.photo_image,
            height=250,
            width=250,
        )
        self.img.grid(column=0, row=1)

        # Image size, label
        self.size_label = ttk.Label(self, text="No Image")
        self.size_label.grid(column=0, row=2)

    def imageGet(self, *args, **kwargs):
        return self.picture

    def imagePathGet(self, *args, **kwargs):
        return self.image_path.get()

    def resetPath(self, *args, **kwargs):
        self.image_path.set("")

    def imageLoad(self, *args, **kwargs):
        """
        Loads the first image binded to the selected files and checks if
        they are all the same. If not then it loads no image.
        Also does nothing if the file doesnt have an image attached.
        """
        # Error handling if theres no image
        try:
            selection = bpn.fn_treeview.selectedItems()

            # Load the first image, and well use it to compare against
            self.picture = utils.meta_picture(selection[0])

            # If the selected file isnt valid
            if self.picture == "not valid":
                # set the size label to show such message
                self.size_label.config(text="Not a valid file")
                self.picture = None

            # Else if checks against that first loaded image every other image
            # When it finds a diferent image breaks out of the loop and
            # executes the if
            elif not all(
                utils.meta_picture(file) == self.picture for file in selection
            ):
                self.size_label.config(text="Different images")
                self.picture = None

        except (IndexError, AttributeError):
            # Set the size label to show theres no image
            self.size_label.config(text="No image")

    def imageShow(self, *args, **kwargs):
        """Shows the first image binded to the files"""
        self.picture = None
        self.imageLoad()
        if self.picture is not None:
            im = PIL.Image.open(BytesIO(self.picture))
            # Get image size before resizing
            im_width, im_height = map(str, im.size)

            # Resize
            # im = im.resize((250, 250), PIL.Image.ANTIALIAS)
            im = im.resize((250, 250), PIL.Image.LANCZOS)

            # Show image
            render = PIL.ImageTk.PhotoImage(im)
            self.img.image = render
            self.img.config(image=render)

            # Show image size
            size_text = "{} x {}".format(im_width, im_height)
            self.size_label.config(text=size_text)

        else:
            self.img.config(image=self.photo_image)
