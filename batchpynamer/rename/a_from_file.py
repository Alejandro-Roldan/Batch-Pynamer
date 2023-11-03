import os

import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class RenameFromFile(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (0)
    """
    Draws the Rename from file widget. Inside the rename notebook.
    This takes priority over anything else
    It has:
        - An entry to enter the path to the text file to rename from
        - A checkbutton to select if you want to wrap around once the end
        of the file is reached
    """

    def __init__(self):
        pass

    def tk_init(self, master, **kwargs):
        super().__init__(master, text="Rename From File (0)", **kwargs)
        self.grid(column=0, row=0, sticky="nsew")

        # Variable defs
        self.fields = self.Fields(
            rename_from_file_file=(tk.StringVar(), ""),
            rename_from_file_wrap=(tk.BooleanVar(), False),
        )
        # Filename, entry
        ttk.Label(self, text="Filename").grid(column=0, row=0, sticky="w")
        self.file_entry = ttk.Entry(
            self, width=10, textvariable=self.fields.rename_from_file_file
        )
        self.file_entry.grid(column=1, row=0, sticky="ew")

        # Wrap, checkbutton
        self.wrap_check = ttk.Checkbutton(
            self,
            text="Wrap",
            variable=self.fields.rename_from_file_wrap,
        )
        self.wrap_check.grid(column=0, row=1)

        # Reset, button
        self.reset_button = ttk.Button(
            self, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)

        self.bindEntries()

    # def fileGet(self, *args, **kwargs):
    #     return self.file.get()

    # def wrapGet(self, *args, **kwargs):
    #     return self.wrap.get()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        # Calls to update the new name column
        self.fields.rename_from_file_file.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.rename_from_file_wrap.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.file.set("")
    #     self.wrap.set(False)

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.file.set(var_dict["rename_from_file_file"])
    #     self.wrap.set(var_dict["rename_from_file_wrap"])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_["rename_from_file_file"] = nb.rename_from_file.fileGet()
        dict_["rename_from_file_wrap"] = nb.rename_from_file.wrapGet()


def rename_from_file_rename(name, idx, **fields_dict):
    """
    Get the file to extract the names from, open it and match the names
    one to one per index base
    """
    rename_from_file_file = fields_dict.get("rename_from_file_file")
    rename_from_file_wrap = fields_dict.get("rename_from_file_wrap")

    if os.path.exists(rename_from_file_file):
        try:
            with open(rename_from_file_file, "r") as f:
                lines = f.readlines()
                lines_count = len(lines)
                try:
                    if rename_from_file_wrap:
                        name = lines[idx % lines_count]
                    else:
                        name = lines[idx]
                except IndexError:
                    pass
        except IsADirectoryError:
            pass

    return name
