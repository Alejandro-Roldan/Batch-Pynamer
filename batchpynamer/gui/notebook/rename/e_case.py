import tkinter as tk
from tkinter import ttk

from batchpynamer.gui.basewidgets import BaseNamingWidget, BpnComboVar


class Case(BaseNamingWidget, ttk.LabelFrame):  # (4)
    """
    Draws the Case changer widget. Inside rename notebook.
    4th thing to change.
    It has:
        - Combobox to choose what case to use (same, upper, lower, title)
        - Reset button
    """

    def __init__(self):
        self.fields = self.Fields(
            case_case_want=BpnComboVar(
                ("Same", "Upper Case", "Lower Case", "Title", "Sentence")
            ),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=1,
            text="Case (4)",
        )
        super().tk_init()

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

        self.bindings()
