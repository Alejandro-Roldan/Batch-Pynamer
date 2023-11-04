from tkinter import ttk
import tkinter as tk

import batchpynamer

from .. import basewidgets


class FiltersWidget(basewidgets.BaseNamingWidget, ttk.LabelFrame):
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
            mask=(tk.StringVar(), ""),
            ext=(tk.StringVar(), ""),
            folders=(tk.BooleanVar(value=True), True),
            files=(tk.BooleanVar(value=True), True),
            hidden=(tk.BooleanVar(value=False), False),
            files_before_dirs=(tk.BooleanVar(value=False), False),
            reverse=(tk.BooleanVar(value=False), False),
            min_name_len=(tk.IntVar(value=0), 0),
            max_name_len=(
                tk.IntVar(value=batchpynamer.MAX_NAME_LEN),
                batchpynamer.MAX_NAME_LEN,
            ),
            depth=(tk.IntVar(value=0), 0),
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
            to=batchpynamer.MAX_NAME_LEN,
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
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.min_name_len,
        )
        self.name_len_min_spin.grid(column=7, row=1, sticky="w")

        # Maximum name lenght, spinbox
        ttk.Label(self, text="max").grid(column=8, row=1, sticky="e")
        self.name_len_max_spin = ttk.Spinbox(
            self,
            width=3,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.max_name_len,
        )
        self.name_len_max_spin.grid(column=9, row=1, sticky="w")

        self.bindEntries()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        self.mask_entry.bind(
            "<FocusOut>", batchpynamer.fn_treeview.refreshView
        )
        self.mask_entry.bind("<Return>", batchpynamer.fn_treeview.refreshView)
        self.ext_entry.bind("<FocusOut>", batchpynamer.fn_treeview.refreshView)
        self.ext_entry.bind("<Return>", batchpynamer.fn_treeview.refreshView)
        self.fields.folders.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.files.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.hidden.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.hidden.trace_add(
            "write", batchpynamer.folder_treeview.refreshView
        )
        self.fields.files_before_dirs.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.reverse.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.min_name_len.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.max_name_len.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
        self.fields.depth.trace_add(
            "write", batchpynamer.fn_treeview.refreshView
        )
