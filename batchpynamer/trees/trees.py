import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.basewidgets import BaseWidget


class TreesFrame(BaseWidget, ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(1, weight=1)

        bpn.fn_treeview.tk_init(self)
        bpn.folder_treeview.tk_init(self, path=bpn.OG_PATH)
        bpn.dir_entry_frame.tk_init(self)


def refresh_treeviews():
    """Refreshes Both Treeviews"""
    # Update the file view
    bpn.fn_treeview.refreshView()
    # Update the folder view
    bpn.folder_treeview.updateNode()

    bpn.info_bar.lastActionRefresh("Refreshed Both Treeviews")
