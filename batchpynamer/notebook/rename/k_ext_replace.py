import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from batchpynamer.basewidgets import BaseNamingWidget, BpnComboVar, BpnStrVar


class ExtReplace(BaseNamingWidget, ttk.LabelFrame):  # (10)
    """
    Draws the extension replacer widget. Inside rename notebook.
    10th thing to change.
    It has:
        - Dropdown to choose how to change the extension
            - Same
            - Lower case
            - Upper case
            - Title
            - Extra: adds a new extension at the end
            - Fixed: changes the extension to a new one
            - Remove
        - Entry to write the new extension for the "Extra" and the "Fixed"
        options
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=5,
            row=2,
            text="Extension (10)",
        )
        super().tk_init()

        # Variable defs
        self.fields = self.Fields(
            ext_replace_change_ext=BpnComboVar(
                (
                    "Same",
                    "Lower",
                    "Upper",
                    "Title",
                    "Extra",
                    "Fixed",
                    "Remove",
                )
            ),
            ext_replace_fixed_ext=BpnStrVar(""),
        )

        # Change Extension, combobox
        self.change_ext_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=self.fields.ext_replace_change_ext.options,
            textvariable=self.fields.ext_replace_change_ext,
        )
        self.change_ext_combo.grid(column=0, row=0, sticky="ew")

        # Replace extension with, entry
        self.fixed_ext_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.ext_replace_fixed_ext,
        )
        self.fixed_ext_entry.grid(column=1, row=0, sticky="ew")

        self.bindEntries()


def ext_rename(ext, fields_dict):
    ext_replace_change_ext = fields_dict.get("ext_replace_change_ext")
    ext_replace_fixed_ext = fields_dict.get("ext_replace_fixed_ext")

    if ext_replace_change_ext == "Lower":
        ext = ext.lower()
    elif ext_replace_change_ext == "Upper":
        ext = ext.upper()
    elif ext_replace_change_ext == "Title":
        ext = ext.title()
    elif ext_replace_change_ext == "Extra":
        ext = ext + "." + ext_replace_fixed_ext
    elif ext_replace_change_ext == "Fixed":
        ext = "." + ext_replace_fixed_ext
    elif ext_replace_change_ext == "Remove":
        ext = ""

    return ext
