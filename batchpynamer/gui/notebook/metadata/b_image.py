import logging
import tkinter as tk
from io import BytesIO
from tkinter import ttk

import PIL
import PIL.ImageTk

import batchpynamer.gui as bpn_gui
from batchpynamer.data import metadata_data_tools
from batchpynamer.gui.basewidgets import BaseFieldsWidget, BpnStrVar

IMG_DISPLAY_SIZE = 310  # Max size before it makes the window bigger


class MetadataImg(BaseFieldsWidget, ttk.Frame):
    """
    Draws the Metadata Image widget. Inside metadata notebook.
    It has:
        - An entry to write the path to the new image
        - A X button to empty the new image entry
        - A canvas to display the metadata image
    """

    # For the display size
    img_display_size = IMG_DISPLAY_SIZE
    # And the image resizing to fit
    img_display_h_w = (
        img_display_size,
        img_display_size,
    )
    picture = None

    def __init__(self):
        self.fields = self.Fields(
            image_path=BpnStrVar(""),
            # Empty photo image to force the label to use pixel size
            photo_image=tk.PhotoImage(),
        )

    def tk_init(self, master):
        super().__init__(master, column=1, row=0, sticky="nsew")

        # Path to new image, entry
        self.image_path_entry = ttk.Entry(
            self, textvariable=self.fields.image_path
        )
        self.image_path_entry.grid(column=0, row=0, sticky="ew")

        self.reset_path_button = ttk.Button(
            self,
            width=2,
            text="X",
            command=lambda: self.fields.image_path.set(
                self.fields.image_path.default
            ),
        )
        self.reset_path_button.grid(column=1, row=0, sticky="w")

        # Image frame, Label
        self.img = tk.Label(
            self,
            relief="sunken",
            background="gray10",
            image=self.fields.photo_image,
            height=self.img_display_size,
            width=self.img_display_size,
        )
        self.img.grid(column=0, row=1)

        # Image size, label
        self.size_label = ttk.Label(self, text="No Image")
        self.size_label.grid(column=0, row=2)

    def image_gui_show(self):
        """Shows the first image binded to the files"""

        def _compare_img(selection):
            """
            Checks all images are the same. If not then it loads no image.
            Also does nothing if the file doesnt have an image attached.
            """
            try:
                if not selection:
                    raise IndexError
                # Load images into a set (they cant have duplicate items) to
                # check all images are the same
                pic_set = set()
                for file in selection:
                    # IndexError raises if no image for flac
                    # or AttributeError raises if no image in mp3
                    pic_set.add(metadata_data_tools.meta_img_get(file))
                    # As soon as there are more, exit
                    if len(pic_set) > 1:
                        return None, "Different images"
            except (IndexError, AttributeError):
                return None, "No image"
            else:
                picture1 = pic_set.pop()
                if picture1 == "not valid":
                    return None, "Not a valid file"
                else:
                    # PIL to get image size and resize
                    picture1 = PIL.Image.open(BytesIO(picture1))
                    im_width, im_height = map(str, picture1.size)
                    picture1 = picture1.resize(
                        self.img_display_h_w, PIL.Image.LANCZOS
                    )
                    # Create a Tkinter usable image from PIL object
                    picture1 = PIL.ImageTk.PhotoImage(picture1)

                    return picture1, f"{im_width} x {im_height}"

        selection = bpn_gui.fn_treeview.selection_get()

        # Get the display img and text
        self.picture, text = _compare_img(selection)

        if self.picture is not None:
            # Set this so it doesnt get garbage collected and dissapears
            self.img.image = self.picture
        else:
            # But here we dont add that so it does get garbage collected
            # And we set the picture to the empty image
            self.picture = self.fields.photo_image

        # Display the image
        self.img.config(image=self.picture)
        # And update label text
        self.size_label.config(text=text)
        logging.debug("GUI- image- " + text)
