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

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Case (4)")
        self.lf.grid(column=0, row=1, sticky="nsew")

        # Variable defs
        # self.case_case_want = tk.StringVar()
        self.fields = self.Fields(
            case_case_want=(
                tk.StringVar(),
                ("Same", "Upper Case", "Lower Case", "Title", "Sentence"),
            ),
        )

        # Chose case, combobox
        ttk.Label(self.lf, text="Case").grid(column=0, row=0, sticky="w")
        self.case_combo = ttk.Combobox(
            self.lf,
            width=10,
            state="readonly",
            # values=("Same", "Upper Case", "Lower Case", "Title", "Sentence"),
            values=self.fields.case_case_want.default,
            textvariable=self.fields.case_case_want,
        )
        self.case_combo.grid(column=1, row=0, sticky="ew")
        self.case_combo.current(0)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=2, row=1, sticky="e", padx=2, pady=2)

        self.bindEntries()

    # def caseWantGet(self, *args, **kwargs):
    #     return self.case_case_want.get()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        self.case_combo.bind("<<ComboboxSelected>>", self.defocus)

        # Calls to update the new name column
        self.fields.case_case_want.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.case_combo.selection_clear()

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.case_case_want.set("Same")

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.case_case_want.set(var_dict["case_case_want"])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_["case_case_want"] = nb.case.caseWantGet()


def case_change(name, **fields_dict):
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
