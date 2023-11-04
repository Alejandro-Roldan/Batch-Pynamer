import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from ..basewidgets import BaseNamingWidget, BpnComboVar, BpnStrVar


class NameBasic(BaseNamingWidget, ttk.LabelFrame):  # (2)
    """
    Draws the Name widget. Inside the rename notebook. 2nd thing to change.
    It has:
        - A dropdown that lets you choose an option that affects
        the whole name
            - Keep: no change
            - Remove: compleatly erase the filename
            - Reverse: reverses the name, e.g. 12345.txt becomes 54321.txt
            - Fixed: specify a new name in the entry
        - An entry that lets you specify a name for all selected items
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=2,
            row=0,
            text="Name (2)",
        )
        super().tk_init()

        # Variable defs
        self.fields = self.Fields(
            name_basic_name_opt=BpnComboVar(
                ("Keep", "Remove", "Reverse", "Fixed")
            ),
            name_basic_fixed_name=BpnStrVar(""),
        )

        # Chose case, combobox
        ttk.Label(self, text="Name").grid(column=0, row=0, sticky="w")
        self.name_opt_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=self.fields.name_basic_name_opt.options,
            textvariable=self.fields.name_basic_name_opt,
        )
        self.name_opt_combo.grid(column=1, row=0, sticky="ew")

        # Replace this, entry
        self.fixed_name_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.name_basic_fixed_name,
        )
        self.fixed_name_entry.grid(column=1, row=1, sticky="ew")

        self.bindEntries()


def name_basic_rename(name, fields_dict):
    """Self explanatory"""
    name_basic_name_opt = fields_dict.get("name_basic_name_opt")

    if name_basic_name_opt == "Remove":
        name = ""
    elif name_basic_name_opt == "Reverse":
        name = name[::-1]
    elif name_basic_name_opt == "Fixed":
        name = fields_dict.get("name_basic_fixed_name")

    return name
