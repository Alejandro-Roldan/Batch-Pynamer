import os

import batchpynamer.gui as bpn_gui
from batchpynamer.data.metadata_data_tools import meta_audio_get
from batchpynamer.data.rename_data_tools import rename_ext_split_action
from batchpynamer.gui.infobar import finish_show_working
from batchpynamer.gui.notebook import notebook
from batchpynamer.plugins.plugins_base import BasePlugin


class _MetadataPluginBaseClass(BasePlugin):
    # def run(self, item: os.DirEntry):
    def run(self, item, **kwargs):
        if os.path.isfile(item):
            # Get the metadata and call changes
            meta_audio = meta_audio_get(item)
            meta_audio = self.meta_changes(meta_audio, item)

            meta_audio.save()

    def meta_changes(self, meta_audio):
        raise NotImplementedError

    def post_hook(self, run_return=None, pre_hook_return=None):
        if bpn_gui.root:
            notebook.populate_fields()

            finish_show_working(inf_msg=self.finish_msg)


class TitleTrackFromFile(_MetadataPluginBaseClass):
    """
    Sets the title and tracknumber metadata getting its values from the
    filename. It splits the filename at the first apparition of "-" and
    sets the left part to be the tracknumber and the right part to be
    the title.
    """

    short_description = 'Set "title" & "tracknumber" from filename'
    finish_msg = 'Changed "title" and "tracknumber" according to filename'
    allow_no_selection = False

    def meta_changes(self, meta_audio, item):
        # Get the filename
        # TODO: get name from data module
        name = os.path.basename(item)

        # Split filename
        n, title = name.split("-", 1)
        # Remove the extension from the title
        title, ext = rename_ext_split_action(title)

        # Set the new metadata values
        meta_audio["title"] = title.strip()
        meta_audio["tracknumber"] = n.strip()

        return meta_audio


class FormatTrackNumMeta(_MetadataPluginBaseClass):
    """Format metadata's tracknumber to be a single 2 digits number"""

    short_description = 'Format "tracknumber"'
    finish_msg = 'Changed "tracknumber" format'

    def meta_changes(self, meta_audio, _):
        # Specifically the tracknumber (which is a list so get the first item)
        n = meta_audio["tracknumber"][0]

        # Remove everything after "/" (inclusive)
        n = n.partition("/")[0]
        # Add left padding of 0s
        n = n.rjust(2, "0")

        # Set the tracknumber
        meta_audio["tracknumber"] = n

        return meta_audio
