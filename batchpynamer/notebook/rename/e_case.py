import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn

from batchpynamer.basewidgets import BaseNamingWidget, BpnComboVar


class Case(BaseNamingWidget, ttk.LabelFrame):  # (4)
    """
    Draws the Case changer widget. Inside rename notebook.
    4th thing to change.
    It has:
        - Combobox to choose what case to use (same, upper, lower, title)
        - Reset button
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=1,
            text="Case (4)",
        )
        super().tk_init()

        # Variable defs
        self.fields = self.Fields(
            case_case_want=BpnComboVar(
                ("Same", "Upper Case", "Lower Case", "Title", "Sentence")
            ),
        )

        # Chose case, combobox
        ttk.Label(self, text="Case").grid(column=0, row=0, sticky="w")
        self.case_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=self.fields.case_case_want.options,
            textvariable=self.fields.case_case_want,
        )
        self.case_combo.grid(column=1, row=0, sticky="ew")

        self.bindEntries()


def case_change(name, fields_dict):
    """Does the case change for the new name"""
    case_case_want = fields_dict.get("case_case_want")

    if case_case_want == "Upper Case":
        name = name.upper()

    elif case_case_want == "Lower Case":
        name = name.lower()

    elif case_case_want == "Title":
        name = name.title()

    elif case_case_want == "Sentence":
        name = name.capitalize()

    return name
