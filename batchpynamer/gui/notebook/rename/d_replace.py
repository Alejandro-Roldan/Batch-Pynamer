import tkinter as tk
from tkinter import ttk

from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnStrVar,
)


class Replace(BaseNamingWidget, ttk.LabelFrame):  # (3)
    """
    Draws the replace widget. Inside rename notebook. 3rd thing to change.
    It has:
        - Entry to choose char(s) to replace
        - Entry for what to replace those char(s) with
        - Reset button
    """

    def __init__(self):
        self.fields = self.Fields(
            replace_replace_this=BpnStrVar(""),
            replace_replace_with=BpnStrVar(""),
            replace_match_case=BpnBoolVar(False),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=1,
            row=1,
            columnspan=2,
            text="Replace (3)",
        )
        super().tk_init()

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

        self.bindings()
