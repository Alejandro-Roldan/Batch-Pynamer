from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseWidget


class TreesFrame(BaseWidget, ttk.Frame):
    def __init__(self, master, og_path, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        bpn_gui.folder_treeview.tk_init(self, path=og_path)
        bpn_gui.fn_treeview.tk_init(self)
        bpn_gui.dir_entry_frame.tk_init(self)


def refresh_file_navigator_view(
    var=None, index=None, mode=None, event=None, new_active_path=None
):
    """Refreshes file navigation (right) treeview"""

    bpn_gui.dir_entry_frame.active_path_set(new_active_path=new_active_path)
    bpn_gui.info_bar.last_action_set("Refreshed File Navigator Treeview")


def refresh_folderview_focus_node(var=None, index=None, mode=None, event=None):
    """Refreshes the focused folder in the navigation (left) treeview"""

    bpn_gui.folder_treeview.update_active_node_call()
    bpn_gui.info_bar.last_action_set("Refreshed Focused Directory in Treeview")


def refresh_folderview_full_tree(var=None, index=None, mode=None, event=None):
    """Refreshes the folder navigation (left) treeview"""

    bpn_gui.folder_treeview.refresh_full_tree_call()
    bpn_gui.info_bar.last_action_set("Refreshed Browse Files Treeview")


def refresh_treeviews(var=None, index=None, mode=None, event=None):
    """Refreshes Both Treeviews"""

    # Update the folder view
    refresh_folderview_focus_node()
    # Update the file view
    refresh_file_navigator_view()
    bpn_gui.info_bar.last_action_set("Refreshed Both Treeviews")
