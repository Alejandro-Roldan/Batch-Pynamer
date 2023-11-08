from batchpynamer.plugins.plugins_base import BasePlugin

import time
import pathlib
import shutil


class DeleteSelection(BasePlugin):
    """Deletes the selection. files and empty dirs."""

    short_desc = "Delete Selection"
    finished_msg = "Deleted"

    def run(self, item):
        try:
            pathlib.Path.unlink(item, missing_ok=True)
        except IsADirectoryError:
            try:
                pathlib.Path.rmdir(item)
            # Directory not empty
            except OSError:
                pass


class ForceDeleteSelection(BasePlugin):
    """Also deletes non empty dirs"""

    short_desc = "Force Delete Selection"
    finished_msg = "Deleted"

    def run(self, item):
        try:
            pathlib.Path.unlink(item, missing_ok=True)
        except IsADirectoryError:
            shutil.rmtree(item)
