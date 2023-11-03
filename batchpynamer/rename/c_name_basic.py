import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class NameBasic(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (2)
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
        self.fields = self.Fields(
            name_basic_name_opt=(
                tk.StringVar(),
                ("Keep", "Remove", "Reverse", "Fixed"),
            ),
            name_basic_fixed_name=(tk.StringVar(), ""),
        )

    def tk_init(self, master, **kwargs):
        super().__init__(master, text="Name (2)", **kwargs)
        self.grid(column=2, row=0, sticky="nsew")

        # Chose case, combobox
        ttk.Label(self, text="Name").grid(column=0, row=0, sticky="w")
        self.name_opt_combo = ttk.Combobox(
            self,
            width=10,
            state="readonly",
            # values=("Keep", "Remove", "Reverse", "Fixed"),
            values=self.fields.name_basic_name_opt.default,
            # textvariable=self.name_basic_name_opt,
            textvariable=self.fields.name_basic_name_opt,
        )
        self.name_opt_combo.grid(column=1, row=0, sticky="ew")
        self.name_opt_combo.current(0)

        # Replace this, entry
        self.fixed_name_entry = ttk.Entry(
            self, width=10, textvariable=self.fields.name_basic_fixed_name
        )
        self.fixed_name_entry.grid(column=1, row=1, sticky="ew")

        # Reset, button
        self.reset_button = ttk.Button(
            self, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)

        self.bindEntries()

    def bindEntries(self):
        """Defines the binded actions"""
        self.name_opt_combo.bind("<<ComboboxSelected>>", self.defocus)

        # Calls to update the new name column
        self.fields.name_basic_name_opt.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.name_basic_fixed_name.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, event=None):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.name_opt_combo.selection_clear()

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.fields.name_basic_name_opt.set("Keep")
    #     self.fields.name_basic_fixed_name.set("")

    def setCommand(self, var_dict, *args, **kwargs):
        """
        Sets the variable fields according to the loaded
        command dictionary
        """
        self.fields.name_basic_name_opt.set(var_dict["name_basic_name_opt"])
        self.fields.name_basic_fixed_name.set(
            var_dict["name_basic_fixed_name"]
        )

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_["name_basic_name_opt"] = nb.name_basic.nameOptGet()
        dict_["name_basic_fixed_name"] = nb.name_basic.fixedNameGet()


def name_basic_rename(name, **fields_dict):
    """Self explanatory"""
    name_basic_name_opt = fields_dict.get("name_basic_name_opt")

    if name_basic_name_opt == "Remove":
        name = ""
    elif name_basic_name_opt == "Reverse":
        name = name[::-1]
    elif name_basic_name_opt == "Fixed":
        name = fields_dict.get("name_basic_fixed_name")

    return name
