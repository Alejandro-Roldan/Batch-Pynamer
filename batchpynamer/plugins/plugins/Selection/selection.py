import logging
import os
import time

import batchpynamer.gui as bpn_gui
from batchpynamer.gui import infobar
from batchpynamer.plugins.plugins_base import BasePlugin


class _SelectionPluginBaseClass(BasePlugin):
    finished_msg = "Selected"

    def selection(self):
        return bpn_gui.fn_treeview.tree_folder.get_children()

    def post_hook(self):
        logging.info(self.finished_msg)
        bpn_gui.fn_treeview.selection_set(self.run_return)
        infobar.finish_show_working(inf_msg=self.finished_msg)


class SelectMTimeToday(_SelectionPluginBaseClass):
    short_desc = "Select last modified 24h"

    def run(self, item):
        mod_time = os.stat(item).st_mtime
        yesterday = time.time() - 24 * 60 * 60
        if mod_time >= yesterday:
            return item
