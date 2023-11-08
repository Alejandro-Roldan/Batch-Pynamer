import logging
import os
from tkinter import ttk

import batchpynamer.gui as bpn_gui
from batchpynamer.gui.basewidgets import BaseFieldsWidget, BpnStrVar
from batchpynamer.gui.trees import trees


class DirectoryEntryFrame(BaseFieldsWidget, ttk.Frame):
    """
    Draws a entry field that has the active directory path, and that can
    be used to go to an specific directory directly by writing on it and
    using ENTER.
    It also has a R button to refresh the directory navigator.
    One click refreshes the active node, two the whole tree.
    """

    def __init__(self):
        self.fields = self.Fields(active_path=BpnStrVar(""))

    def tk_init(self, master, **kwargs):
        super().__init__(
            master=master,
            column=0,
            row=0,
            columnspan=2,
            sticky="we",
            **kwargs,
        )
        # Set the weight of the entry column so it extends the whole frame
        self.columnconfigure(1, weight=1)

        # Folder Navigation Refresh, button
        self.folder_nav_refresh_button = ttk.Button(self, width=2, text="R")
        self.folder_nav_refresh_button.grid(column=0, row=0, sticky="w")

        # Folder path, entry
        self.folder_dir_entry = ttk.Entry(
            self, textvariable=self.fields.active_path
        )
        self.folder_dir_entry.grid(column=1, row=0, sticky="w" + "e")

        self.bindings()

    def bindings(self):
        self.folder_dir_entry.bind("<Return>", self.active_path_set)
        self.folder_nav_refresh_button.bind(
            "<Button-1>", trees.refresh_folderview_focus_node
        )
        self.folder_nav_refresh_button.bind(
            "<Double-1>", trees.refresh_folderview_full_tree
        )

    def active_path_set(
        self, var=None, index=None, mode=None, event=None, new_active_path=None
    ):
        """Sets the active path and refreshes the file view"""
        if new_active_path is not None:
            self.fields.active_path.set(new_active_path)

        active_path = self.fields.active_path.get()

        if os.path.isdir(active_path):
            bpn_gui.fn_treeview.refresh_view_call(active_path)
        else:
            bpn_gui.info_bar.last_action_set("Not a Valid Directory")
            logging.warning(f'GUI- "{active_path}" not a valid directory')
