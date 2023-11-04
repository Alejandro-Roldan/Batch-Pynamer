import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnIntVar,
    BpnStrVar,
)


class FiltersWidget(BaseNamingWidget, ttk.LabelFrame):
    """
    Draws the filter widget. Inside rename notebook.
    It has:
        - A regular expression mask entry
        - A extension list entry
        - A folders checkbutton
        - A files checkbutton
        - A Files before Directories checkbutton
        - A hidden files checkbutton
        - A minimum name length spinbox
        - A maximum name lenght spinbox
        - A recursive depth level spinbox
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=0,
            sticky="w",
            text="Filter File View",
        )
        super().tk_init(reset_column_row=(10, 1))

        # Variable defs
        self.fields = self.Fields(
            mask=BpnStrVar(""),
            ext=BpnStrVar(""),
            folders=BpnBoolVar(True),
            files=BpnBoolVar(True),
            hidden=BpnBoolVar(False),
            files_before_dirs=BpnBoolVar(False),
            reverse=BpnBoolVar(False),
            min_name_len=BpnIntVar(0),
            max_name_len=BpnIntVar(bpn.MAX_NAME_LEN),
            depth=BpnIntVar(0),
        )

        # Regular expression mask, entry
        ttk.Label(self, text="Mask").grid(column=0, row=0, sticky="e")
        self.mask_entry = ttk.Entry(
            self, width=10, textvariable=self.fields.mask
        )
        self.mask_entry.grid(column=1, row=0, sticky="w")

        # Extension list, entry
        ttk.Label(self, text="Ext(s)").grid(column=0, row=1, sticky="e")
        self.ext_entry = ttk.Entry(
            self, width=10, textvariable=self.fields.ext
        )
        self.ext_entry.grid(column=1, row=1, sticky="w")

        # Folders, checkbutton
        self.folders_check = ttk.Checkbutton(
            self,
            text="Folders",
            variable=self.fields.folders,
        )
        self.folders_check.grid(column=2, row=0, sticky="w")

        # Files, checkbutton
        self.files_check = ttk.Checkbutton(
            self,
            text="Files",
            variable=self.fields.files,
        )
        self.files_check.grid(column=2, row=1, sticky="w")

        # Hidden files, checkbutton
        self.hidden_check = ttk.Checkbutton(
            self,
            text="Hidden",
            variable=self.fields.hidden,
        )
        self.hidden_check.grid(column=3, row=0, sticky="w")

        # Reverse files, checkbutton
        self.reverse_check = ttk.Checkbutton(
            self,
            text="Reverse",
            variable=self.fields.reverse,
        )
        self.reverse_check.grid(column=3, row=1, sticky="w")

        # Files before directories, checkbutton
        self.files_before_dirs_check = ttk.Checkbutton(
            self,
            text="Files before Dirs",
            variable=self.fields.files_before_dirs,
        )
        self.files_before_dirs_check.grid(
            column=4, row=1, columnspan=2, sticky="w"
        )

        # Recursive depth levels, spinbox
        ttk.Label(self, text="Recursive Levels").grid(
            column=4, row=0, sticky="ew"
        )
        self.depth_spin = ttk.Spinbox(
            self,
            width=3,
            from_=-1,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.depth,
        )
        self.depth_spin.grid(column=5, row=0)

        # Name lenght group
        ttk.Label(self, text="Name lenght").grid(column=6, row=0, columnspan=4)

        # Minimum name lenght, spinbox
        ttk.Label(self, text="min").grid(column=6, row=1, sticky="e")
        self.name_len_min_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.min_name_len,
        )
        self.name_len_min_spin.grid(column=7, row=1, sticky="w")

        # Maximum name lenght, spinbox
        ttk.Label(self, text="max").grid(column=8, row=1, sticky="e")
        self.name_len_max_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.max_name_len,
        )
        self.name_len_max_spin.grid(column=9, row=1, sticky="w")

        self.bindings()

    def bindings(self):
        """Redefined"""
        # Refresh files view when updating fields
        for field in self.fields.__dict__:
            # Except "mask" and "ext" fields
            if field != "mask" and field != "ext":
                self.fields.__dict__[field].trace_add(
                    "write", bpn.fn_treeview.refreshView
                )

        # Those are updated when we finish changing them
        # (instead of with each keystroke)
        self.mask_entry.bind("<FocusOut>", bpn.fn_treeview.refreshView)
        self.mask_entry.bind("<Return>", bpn.fn_treeview.refreshView)
        self.ext_entry.bind("<FocusOut>", bpn.fn_treeview.refreshView)
        self.ext_entry.bind("<Return>", bpn.fn_treeview.refreshView)

        # Refresh folders view
        self.fields.hidden.trace_add("write", bpn.folder_treeview.refreshView)
