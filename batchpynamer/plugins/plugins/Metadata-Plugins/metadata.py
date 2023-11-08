import os

import batchpynamer.gui as bpn_gui
from batchpynamer.data.metadata_data_tools import meta_audio_get, meta_img_get
from batchpynamer.data.rename_data_tools import rename_ext_split_action
from batchpynamer.gui.infobar import finish_show_working
from batchpynamer.gui.notebook import notebook
from batchpynamer.plugins.plugins_base import BasePlugin


class _MetadataPluginBaseClass(BasePlugin):
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


class TitleAndTrackFromFilename(_MetadataPluginBaseClass):
    """
    Sets the title and tracknumber metadata getting its values from the
    filename. It splits the filename at the first apparition of "-" and
    sets the left part to be the tracknumber and the right part to be
    the title.
    """

    finish_msg = 'Changed "title" and "tracknumber" according to filename'

    def meta_changes(self, meta_audio, item):
        # Get the filename
        name = os.path.basename(item)

        # Split filename
        n, title = name.split("-", 1)
        # Remove the extension from the title
        title, ext = rename_ext_split_action(title)

        # Set the new metadata values
        meta_audio["title"] = title.strip()
        meta_audio["tracknumber"] = n.strip()

        return meta_audio


class FormatTrackNum(_MetadataPluginBaseClass):
    """Format metadata's tracknumber to be a single 2 digits number"""

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


class FormatYearDate(_MetadataPluginBaseClass):
    """Format metadata date to just be the year"""

    finish_msg = 'Changed "date" format'

    def meta_changes(self, meta_audio, _):
        try:
            date = meta_audio["date"][0]

            if date.isnumeric():
                meta_audio["date"] = date[:4]
        except KeyError:
            pass

        return meta_audio


class FormatFullDate(_MetadataPluginBaseClass):
    """Format metadata date to have dashes between year-month-day"""

    finish_msg = 'Changed "date" format'

    def meta_changes(self, meta_audio, _):
        try:
            date = meta_audio["date"][0]

            if date.isnumeric() and len(date) == 8:
                date = date[:4] + "-" + date[4:6] + "-" + date[6:]
                meta_audio["date"] = date
        except KeyError:
            pass

        return meta_audio
