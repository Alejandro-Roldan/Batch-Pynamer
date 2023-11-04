import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from batchpynamer.basewidgets import BaseNamingWidget, BpnBoolVar, BpnStrVar


class Replace(BaseNamingWidget, ttk.LabelFrame):  # (3)
    """
    Draws the replace widget. Inside rename notebook. 3rd thing to change.
    It has:
        - Entry to choose char(s) to replace
        - Entry for what to replace those char(s) with
        - Reset button
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=1,
            row=1,
            columnspan=2,
            text="Replace (3)",
        )
        super().tk_init()

        # Variable defs
        self.fields = self.Fields(
            replace_replace_this=BpnStrVar(""),
            replace_replace_with=BpnStrVar(""),
            replace_match_case=BpnBoolVar(False),
        )

        # Replace this, entry
        ttk.Label(self, text="Replace").grid(column=0, row=0, sticky="w")
        self.replace_this_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.replace_replace_this,
        )
        self.replace_this_entry.grid(column=1, row=0, sticky="ew")

        # Replace with, entry
        ttk.Label(self, text="With").grid(column=0, row=1, sticky="w")
        self.replace_with_entry = ttk.Entry(
            self,
            width=10,
            textvariable=self.fields.replace_replace_with,
        )
        self.replace_with_entry.grid(column=1, row=1, sticky="ew")

        # Match case, checkbutton
        self.match_case_check = ttk.Checkbutton(
            self,
            text="Match Case",
            variable=self.fields.replace_match_case,
        )
        self.match_case_check.grid(column=0, row=2)

        self.bindEntries()


def replace_action(name, fields_dict):
    """Does the replace action for the new name"""
    replace_replace_this = fields_dict.get("replace_replace_this")
    replace_replace_with = fields_dict.get("replace_replace_with")
    replace_match_case = fields_dict.get("replace_match_case")

    # When replacing with match case it's a simple matter
    if replace_match_case:
        name = name.replace(replace_replace_this, replace_replace_with)
    # But when replacing without minding the case...
    # (If replace_replace_this is empty it breaks)
    elif replace_replace_this != "":
        # Start searching from the start of the string
        idx = 0
        # Find at what position what we want to replace is (all lowercase)
        # If find returns a -1 it means it didn't find it and we can break
        while (
            idx := name.lower().find(replace_replace_this.lower(), idx) != -1
        ):
            # Create the new name
            name = (
                name[:idx]
                + replace_replace_with
                + name[idx + len(replace_replace_this) :]
            )

            # New index from where to search
            idx = idx + len(replace_replace_with)

    return name
