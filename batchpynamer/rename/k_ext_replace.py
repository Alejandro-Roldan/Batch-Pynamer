# import re  # regular expressions
# import string
import tkinter as tk

# import unicodedata
from tkinter import ttk

import batchpynamer
from .. import basewidgets


class ExtReplace(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (10)
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

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Extension (10)")
        self.lf.grid(column=5, row=2, sticky="nsew")

        # Variable defs
        # self.ext_replace_change_ext = tk.StringVar()
        # self.ext_replace_fixed_ext = tk.StringVar()
        self.fields = self.Fields(
            ext_replace_change_ext=(
                tk.StringVar(),
                (
                    "Same",
                    "Lower",
                    "Upper",
                    "Title",
                    "Extra",
                    "Fixed",
                    "Remove",
                ),
            ),
            ext_replace_fixed_ext=(tk.StringVar(), ""),
        )

        # Change Extension, combobox
        self.change_ext_combo = ttk.Combobox(
            self.lf,
            width=10,
            state="readonly",
            # values=(
            #     "Same",
            #     "Lower",
            #     "Upper",
            #     "Title",
            #     "Extra",
            #     "Fixed",
            #     "Remove",
            # ),
            values=self.fields.ext_replace_change_ext.default,
            textvariable=self.fields.ext_replace_change_ext,
        )
        self.change_ext_combo.grid(column=0, row=0, sticky="ew")
        self.change_ext_combo.current(0)

        # Replace extension with, entry
        self.fixed_ext_entry = ttk.Entry(
            self.lf, width=10, textvariable=self.fields.ext_replace_fixed_ext
        )
        self.fixed_ext_entry.grid(column=1, row=0, sticky="ew")

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=2, row=2, sticky="w", padx=2, pady=2)

        self.bindEntries()

    # def changeExtGet(self, *args, **kwargs):
    #     return self.ext_replace_change_ext.get()

    # def fixedExtGet(self, *args, **kwargs):
    #     return self.ext_replace_fixed_ext.get()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        self.change_ext_combo.bind("<<ComboboxSelected>>", self.defocus)

        # calls to update the new name column
        self.fields.ext_replace_change_ext.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.ext_replace_fixed_ext.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of their changes value.
        """
        self.change_ext_combo.selection_clear()

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.ext_replace_change_ext.set("Same")
    #     self.ext_replace_fixed_ext.set("")

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.ext_replace_change_ext.set(var_dict["ext_replace_change_ext"])
    #     self.ext_replace_fixed_ext.set(var_dict["extension_rep_fixed_ext"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_["ext_replace_change_ext"] = nb.extension_rep.changeExtGet()
    #     dict_["extension_rep_fixed_ext"] = nb.extension_rep.fixedExtGet()


def ext_rename(ext, **fields_dict):
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
