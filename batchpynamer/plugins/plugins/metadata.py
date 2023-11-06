import os

from batchpynamer.data.metadata_data_tools import meta_audio_get
from batchpynamer.data.rename_data_tools import rename_ext_split_action
from batchpynamer.plugins.plugins_base import BasePlugin


class TitleTrackFromFile(BasePlugin):
    """
    Sets the title and tracknumber metadata getting its values from the
    filename. It splits the filename at the first apparition of "-" and
    sets the left part to be the tracknumber and the right part to be
    the title.
    """

    short_description = 'Set "title" & "tracknumber" from filename'
    finish_msg = 'Changed "title" and "tracknumber" according to filename'

    def run(self, item: os.DirEntry):
        if item.isdir():
            # Get the metadata
            meta_audio = meta_audio_get(item.path)
            # Get the filename
            # TODO: get name from data module
            name = item.name

            # Split filename
            n, title = name.split("-", 1)
            # Remove the extension from the title
            title, ext = rename_ext_split_action(title)

            # Set the new metadata values
            meta_audio["title"] = title.strip()
            meta_audio["tracknumber"] = n.strip()

            meta_audio.save()


class FormatTrackNumMeta(BasePlugin):
    """Format metadata's tracknumber to be a single 2 digits number"""

    short_description = 'Format "tracknumber"'
    finish_msg = 'Changed "tracknumber" format'

    def run(self, item: os.DirEntry):
        if item.isdir():
            # Get the metadata
            meta_audio = meta_audio_get(item.path)
            # Specifically the tracknumber (which is a list so get the first item)
            n = meta_audio["tracknumber"][0]

            # Remove everything after "/" (inclusive)
            n = n.partition("/")[0]
            # Add left padding of 0s
            n = n.rjust(2, "0")

            # Set the tracknumber
            meta_audio["tracknumber"] = n
            meta_audio.save()
