import tkinter as tk
from tkinter import ttk

import batchpynamer

from .. import basewidgets


class Case(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (4)
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
        # self.case_case_want = tk.StringVar()
        self.fields = self.Fields(
            case_case_want=(
                tk.StringVar(),
                ("Same", "Upper Case", "Lower Case", "Title", "Sentence"),
            ),
        )

        # Chose case, combobox
        ttk.Label(self, text="Case").grid(column=0, row=0, sticky="w")
        self.case_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            values=self.fields.case_case_want.default,
            textvariable=self.fields.case_case_want,
        )
        self.case_combo.grid(column=1, row=0, sticky="ew")
        self.case_combo.current(0)

        self.bindEntries()

    def bindEntries(self):
        """Defines the binded actions"""
        super().bindEntries()

        # Calls to update the new name column
        self.fields.case_case_want.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )


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
