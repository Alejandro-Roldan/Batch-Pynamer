import os

from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.easymp4 import EasyMP4, EasyMP4KeyError
from mutagen.flac import FLAC
from mutagen.flac import Picture as FlacPicture
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3

import batchpynamer.data as bpn_data


def meta_audio_get(file):
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


def meta_img_get(file):
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


def meta_audio_save(meta_audio, new_metadata_dict: dict):
    for key, value in new_metadata_dict.items():
        if ";" not in value:
            if value:
                try:
                    meta_audio[key] = value
                except (EasyID3KeyError, EasyMP4KeyError):
                    msg = f'Undefined Tag name "{key}" for ID3/MP4. Skipped'
            else:
                del meta_audio[key]

    meta_audio.save()


def meta_img_create(img_path):
    """
    Creates a mutagen.flac.Picture object, sets its mimetype, its
    type and its description. Then loads the selected img and returns
    the Picture object both for flacs and mp3s.
    """
    if not img_path.lower().endswith(bpn_data.IMG_EXTS) or not os.path.isfile(
        img_path
    ):
        return None, None

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


def meta_img_save(item, img=None, apic=None):
    """Changes the image of an audio file"""
    if item.endswith(".flac"):
        meta_audio = FLAC(item)
        meta_img_flac_save(meta_audio, img)
    elif item.endswith(".mp3"):
        meta_audio = ID3(item)
        meta_img_mp3_save(meta_audio, apic)


def meta_img_flac_save(meta_audio, img=None):
    """Changes the image of a flac audio file"""
    if img:
        meta_audio.clear_pictures()  # clear other images
        meta_audio.add_picture(img)  # set new image
        meta_audio.save()


def meta_img_mp3_save(meta_audio, apic=None):
    """Changes the image of a mp3 audio file"""
    if apic:
        for tag in meta_audio:
            if "APIC" in tag:
                meta_audio.delall(tag)
                break
        meta_audio["APIC"] = apic

        meta_audio.save()
