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


class Apply_Changes:
    """
    Apply chnages widget. Inside the metadata notebook.
    It has:
        - Button to apply the metadata changes
        - Button to apply the image changes
        - Button to apply both
    """

    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=2, row=0, sticky="se")

        self.apply_meta_button = ttk.Button(
            self.frame,
            width=10,
            text="Apply Meta",
            command=self.metaChangesCall,
        )
        self.apply_meta_button.grid(column=0, row=0, sticky="e")

        self.apply_img_button = ttk.Button(
            self.frame, width=10, text="Apply Img", command=self.imgChangesCall
        )
        self.apply_img_button.grid(column=0, row=1, sticky="e")

        self.apply_all_button = ttk.Button(
            self.frame, width=10, text="Apply All", command=self.allChangesCall
        )
        self.apply_all_button.grid(column=0, row=2, sticky="e")

    def metaChangesCall(self, *args, **kwargs):
        """
        Calls the procedure to only change metadata tags.
        Loads the new values from the list of entries and sets them up.
        """
        selection = fn_treeview.selectedItems()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Show that its in the process
        Show_Working()

        for item in selection:
            meta_audio = Meta_Audio(item)
            for key in meta_dict:
                value = nb.metadata_list_entries.metaDictTextGet(key)

                self.applyMetaChanges(meta_audio, key, value)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg="Metadata Changed")

    def applyMetaChanges(self, meta_audio, key, value, *args, **kwargs):
        """
        Applies the changes to the metadata. Skips the instances where
        there are several values (so as not to set all values to every
        item) and removes empty tags (if they also exist in the metadata
        tags of the item).
        """
        # If there is more than one value for the field, skip it
        if ";" not in value:
            if value:
                # Tags can have any name in vorbis comment (flac metadata) but
                # not in ID3 (mp3 metadata), so if you try adding a tag with a
                # name thats not accepted in ID3 it'll raise and error
                try:
                    meta_audio[key] = value
                except (EasyID3KeyError, EasyMP4KeyError):
                    msg = (
                        'Undefined Tag name "{}" for ID3/MP4. Skipped'.format(
                            key
                        )
                    )
                    Error_Frame(msg)

            # Delete empty values only when they exist in the metadata
            # of the file
            elif not value and key in meta_audio:
                meta_audio.pop(key)

        meta_audio.save()

    def imgChangesCall(self, *args, **kwargs):
        """
        Calls the procedure to only change the image metadata.
        Loads the new image and then iterates over each item setting
        the picture.
        """
        selection = fn_treeview.selectedItems()
        img_path = nb.metadata_img.imagePathGet()

        # Show that its in the process
        Show_Working()

        if img_path.endswith((".jpg", ".jpeg", ".png")) and os.path.exists(
            img_path
        ):
            # Load the new image
            img, apic = self.loadImage(img_path)
            for item in selection:
                # Load the item metadata and set the new picture.
                if item.endswith(".flac"):
                    meta_audio = FLAC(item)
                    self.applyImgChangesFLAC(meta_audio, img)
                elif item.endswith(".mp3"):
                    meta_audio = ID3(item)
                    self.applyImgChangesMP3(meta_audio, apic)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg="Image Changed")

    def loadImage(self, img_path, *args, **kwargs):
        """
        Creates a mutagen.flac.Picture object, sets its mimetype, its
        type and its description. Then loads the selected img and returns
        the Picture object.
        """
        # Set the corresponding mime type
        if img_path.endswith(".png"):
            mime_type = "image/png"
        else:
            mime_type = "image/jpg"

        # Open bytes like object for the image
        albumart = open(img_path, "rb").read()

        # create img object for flacs and set its properties
        img = FlacPicture()
        # type 3 is for cover image
        img.type = 3
        # Set the corresponding mime type
        img.mime = mime_type
        # Set description
        img.desc = "front cover"
        img.data = albumart

        # Create Image object for mp3s and set its properties
        apic = APIC(
            encoding=3,
            mime=mime_type,
            type=3,
            desc="front cover",
            data=albumart,
        )

        return img, apic

    def applyImgChangesFLAC(self, meta_audio, img=None, *args, **kwargs):
        """Changes the image of a flac audio file"""
        if img:
            meta_audio.clear_pictures()  # clear other images
            meta_audio.add_picture(img)  # set new image
            meta_audio.save()

    def applyImgChangesMP3(self, meta_audio, apic=None, *args, **kwargs):
        """Changes the image of a mp3 audio file"""
        if apic:
            for tag in meta_audio:
                if "APIC" in tag:
                    meta_audio.delall(tag)
                    break
            meta_audio["APIC"] = apic

            meta_audio.save()

    def allChangesCall(self, *args, **kwargs):
        """
        Calls to both the metadata change and the image change
        This is its own defined method and we dont just use the other two
        methods one after the other so as not to loop through all the
        items AND load their metadata twice
        """
        selection = fn_treeview.selectedItems()
        img_path = nb.metadata_img.imagePathGet()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Show that its in the process
        Show_Working()

        if img_path.endswith(("jpg", "jpeg", "png")) and os.path.exists(
            img_path
        ):
            img, apic = self.loadImage(img_path)
        else:
            img = apic = None

        for item in selection:
            # Change the image
            if item.endswith("flac"):
                meta_audio = FLAC(item)
                self.applyImgChangesFLAC(meta_audio, img)
            elif item.endswith("mp3"):
                meta_audio = ID3(item)
                self.applyImgChangesMP3(meta_audio, apic)

            # Load the metadata for flacs and easyid3 for mp3s
            meta_audio = Meta_Audio(item)
            # Change the metadata tags
            for key in meta_dict:
                value = nb.metadata_list_entries.metaDictTextGet(key)

                self.applyMetaChanges(meta_audio, key, value)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg="Metadata and Image Changed")


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


def metadata_rename_format(str_, path, *args, **kwargs):
    """Format the string with the values from the metadata dictionary"""
    # Only load the metadata if the string contains '{' and '}'
    if ("{" and "}") in str_:
        meta_audio = Meta_Audio(path)

        # If the past function returned something (it was a valid file)
        if meta_audio:
            # Get a dict that's the same as meta_audio but only the first
            # item of each key (because the metadata is a dict of lists)
            metadata = {item: meta_audio[item][0] for item in meta_audio}
            # Get a list of the keys in the dict adding the string between
            # curly braces
            field_list = ["{" + key + "}" for key in metadata.keys()]

            # Individually check and replace for each possible key in the dict
            # (need to do this because if you want to use curly braces in the
            # string it would raise an error and would skip any actual editing)
            for field in field_list:
                # **variable unpacks a dictionary into keyword arguments
                # eg: ['a':1, 'b':2] unpacks into function(a=1, b=2)
                # (also *variable unpack a list/tuple into position arguments)
                str_ = str_.replace(field, field.format(**metadata))

    return str_
