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
from batchpynamer import info_bar
from batchpynamer.notebook.utils import de_ext


def meta_audio_get(file, *args, **kwargs):
    """Returns the metadata from the audio file"""
    if file.endswith(".flac"):
        meta_audio = FLAC(file)
    elif file.endswith(".mp3"):
        meta_audio = MP3(file, ID3=EasyID3)
    elif file.endswith(".mp4"):
        meta_audio = EasyMP4(file)
    else:
        meta_audio = None

    return meta_audio


def meta_picture(file, *args, **kwargs):
    """
    Gets the attached picture from the metadata, if there is one, if not
    returns None.
    """
    meta_picture = None
    if file.endswith("flac"):
        meta_picture = FLAC(file).pictures[0].data
    elif file.endswith("mp3"):
        meta_audio = ID3(file)
        # Because the attached picture in mp3 files can have many names
        # and the only common factor is having APIC in the key, check all keys
        # and see if theres any that contains APIC
        for tag in meta_audio:
            if "APIC" in tag:
                meta_picture = meta_audio.get(tag).data
                break
    else:
        meta_picture = "not valid"

    return meta_picture


def no_duplicate_list(list_convert, *args, **kwargs):
    """
    Return a list with no duplicated items
    Typical way to do it would be to convert to set, but sets are not
    ordered, meanwhile a dictionary can only have each key once and
    are ordered (since python 3)
    """
    return list(dict.fromkeys(list_convert))


def title_track_from_file(*args, **kwargs):
    """
    Sets the title and tracknumber metadata getting its values from the
    filename. It splits the filename at the first apparition of "-" and
    sets the left part to be the tracknumber and the right part to be
    the title.
    """
    info_bar.show_working()

    selection = bpn.fn_treeview.selectedItems()

    for item in selection:
        # Get the metadata
        meta_audio = meta_audio_get(item)
        # Get the filename
        name = bpn.fn_treeview.oldNameGet(item)

        # Split filename
        n, title = name.split("-", 1)
        # Remove the extension from the title
        title, ext = rename.de_ext(title)

        # Set the new metadata values
        meta_audio["title"] = title.strip()
        meta_audio["tracknumber"] = n.strip()

        meta_audio.save()

    bpn.changes_notebook.populate_fields()
    msg = 'Changed "title" and "tracknumber" according to filename'
    info_bar.finish_show_working(inf_msg=msg)


def format_track_num_meta(*args, **kwargs):
    """Format metadata's tracknumber to be a single 2 digits number"""
    info_bar.show_working()

    selection = bpn.fn_treeview.selectedItems()

    for item in selection:
        # Get the metadata
        meta_audio = meta_audio_get(item)
        # Specifically the tracknumber (which is a list so get the first item)
        n = meta_audio["tracknumber"][0]

        # Remove everything after "/" (inclusive)
        n = n.partition("/")[0]
        # Add left padding of 0s
        n = n.rjust(2, "0")

        # Set the tracknumber
        meta_audio["tracknumber"] = n
        meta_audio.save()

    bpn.changes_notebook.populate_fields()
    info_bar.finish_show_working(inf_msg='Changed "tracknumber" format')


def metadata_rename_format(str_, path, *args, **kwargs):
    """Format the string with the values from the metadata dictionary"""
    # Only load the metadata if the string contains '{' and '}'
    if ("{" and "}") in str_:
        meta_audio = meta_audio_get(path)

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
