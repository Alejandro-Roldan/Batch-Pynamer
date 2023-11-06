from tkinter import ttk

import batchpynamer as bpn
import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseWidget


class TreesFrame(BaseWidget, ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        bpn_gui.fn_treeview.tk_init(self)
        bpn_gui.folder_treeview.tk_init(self, path=bpn.OG_PATH)
        bpn_gui.dir_entry_frame.tk_init(self)


def refresh_folderview_focus_node(event=None):
    """Refreshes the focused folder in the navigation treeview"""
    bpn_gui.folder_treeview.update_active_node_call()
    bpn_gui.info_bar.last_action_set("Refreshed Focused Directory in Treeview")


def refresh_folderview_full_tree(event=None):
    """Refreshes the folder navigation treeview"""
    bpn_gui.folder_treeview.refresh_full_tree_call()
    bpn_gui.info_bar.last_action_set("Refreshed Browse Files Treeview")


def refresh_treeviews(event=None):
    """Refreshes Both Treeviews"""
    # Update the folder view
    refresh_folderview_focus_node()
    # Update the file view
    bpn_gui.dir_entry_frame.active_path_set()

    bpn_gui.info_bar.last_action_set("Refreshed Both Treeviews")
