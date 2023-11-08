import os

import batchpynamer.gui as bpn_gui
from batchpynamer.data.metadata_data_tools import meta_audio_get
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


class FormatTrackNum(_MetadataPluginBaseClass):
    """Format metadata's tracknumber to be a single 2 digits number"""

    short_desc = 'Format "tracknumber"'
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

    short_desc = 'Format "date" as year'
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

    short_desc = 'Format full "date"'
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
