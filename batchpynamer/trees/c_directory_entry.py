import os
import re
import tkinter as tk
from tkinter import ttk

from scandirrecursive.scandirrecursive import scandir_recursive_sorted

import batchpynamer as bpn
from batchpynamer import basewidgets as bw
from batchpynamer.notebook.rename import rename


class DirectoryEntryFrame(bw.BaseWidget, ttk.Frame):
    """
    Draws a entry field that has the active directory path, and that can
    be used to go to an specific directory directly by writing on it and
    using ENTER.
    It also has a R button to refresh the directory navigator.
    One click refreshes the active node, two the whole tree.
    """

    def __init__(self):
        pass

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

        self.folder_dir = tk.StringVar()

        # Folder Navigation Refresh, button
        self.folder_nav_refresh_button = ttk.Button(self, width=2, text="R")
        self.folder_nav_refresh_button.grid(column=0, row=0, sticky="w")

        # Folder path, entry
        self.folder_dir_entry = ttk.Entry(self, textvariable=self.folder_dir)
        self.folder_dir_entry.grid(column=1, row=0, sticky="w" + "e")

        # self.folder_treeview = folder_treeview
        # self.fn_treeview = fn_treeview
        # self.fn_treeview.directory_entry_frame = self

        # self.info_bar = info_bar

        self.bindings()

    def folderDirGet(self, *args, **kwargs):
        return self.folder_dir.get()

    def bindings(self, *args, **kwargs):
        self.folder_dir_entry.bind("<Return>", self.openFolderTreeNav)
        self.folder_nav_refresh_button.bind(
            "<Button-1>", self.focusFolderRefresh
        )
        self.folder_nav_refresh_button.bind(
            "<Double-1>", self.folderNavRefresh
        )

    def folderNavRefresh(self, *args, **kwargs):
        """Refreshes the folder navigation treeview"""
        # self.folder_treeview.refreshView()
        bpn.folder_treeview.refreshView()
        # self.info_bar.lastActionRefresh("Refreshed Browse Files Treeview")
        bpn.info_bar.lastActionRefresh("Refreshed Browse Files Treeview")

    def focusFolderRefresh(self, *args, **kwargs):
        """Refreshes the focused folder in the navigation treeview"""
        # self.folder_treeview.updateNode()
        bpn.folder_treeview.updateNode()
        # self.info_bar.lastActionRefresh(
        bpn.info_bar.lastActionRefresh(
            "Refreshed Focused Directory in Treeview"
        )

    def folderDirSet(self, *args, **kwargs):
        # folder_path = self.fn_treeview.active_path
        folder_path = bpn.fn_treeview.active_path
        self.folder_dir.set(folder_path)

    def openFolderTreeNav(self, *args, **kwags):
        """Loads the writen path to the file navigator treeview"""
        folder_path = self.folderDirGet()
        # Check if the path is a valid directory
        if os.path.isdir(folder_path):
            # self.fn_treeview.refreshView(path=folder_path)
            bpn.fn_treeview.refreshView(path=folder_path)
        else:
            # self.info_bar.lastActionRefresh("Not a Valid Directory")
            bpn.info_bar.lastActionRefresh("Not a Valid Directory")
            self.folderDirSet()
