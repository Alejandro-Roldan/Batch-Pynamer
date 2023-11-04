import PIL
import PIL.ImageTk
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.easymp4 import EasyMP4, EasyMP4KeyError

# Change import name for code clarity
from mutagen.flac import FLAC
from mutagen.flac import Picture as FlacPicture
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3


def Meta_Audio(file, *args, **kwargs):
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


def Meta_Picture(file, *args, **kwargs):
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
