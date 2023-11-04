import os
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.basewidgets import BaseNamingWidget, BpnBoolVar, BpnStrVar


class RenameFromFile(BaseNamingWidget, ttk.LabelFrame):  # (0)
    """
    Draws the Rename from file widget. Inside the rename notebook.
    This takes priority over anything else
    It has:
        - An entry to enter the path to the text file to rename from
        - A checkbutton to select if you want to wrap around once the end
        of the file is reached
    """

    def __init__(self):
        self.fields = self.Fields(
            rename_from_file_file=BpnStrVar(""),
            rename_from_file_wrap=BpnBoolVar(False),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=0,
            text="Rename From File (0)",
        )
        super().tk_init()

        # Variable defs
        # self.fields = self.Fields(
        #     rename_from_file_file=BpnStrVar(""),
        #     rename_from_file_wrap=BpnBoolVar(False),
        # )

        # Filename, entry
        ttk.Label(self, text="Filename").grid(column=0, row=0, sticky="w")
        self.file_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.rename_from_file_file,
        )
        self.file_entry.grid(column=1, row=0, sticky="ew")

        # Wrap, checkbutton
        self.wrap_check = ttk.Checkbutton(
            self,
            text="Wrap",
            variable=self.fields.rename_from_file_wrap,
        )
        self.wrap_check.grid(column=0, row=1)

        self.bindings()


def rename_from_file_rename(name, idx, fields_dict):
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
