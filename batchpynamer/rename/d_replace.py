import tkinter as tk
from tkinter import ttk

import batchpynamer
from .. import basewidgets


class Replace(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (3)
    """
    Draws the replace widget. Inside rename notebook. 3rd thing to change.
    It has:
        - Entry to choose char(s) to replace
        - Entry for what to replace those char(s) with
        - Reset button
    """

    def __init__(self):
        pass

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Replace (3)")
        self.lf.grid(column=1, row=1, columnspan=2, sticky="nsew")

        # Variable defs
        # self.replace_replace_this = tk.StringVar()
        # self.replace_replace_with = tk.StringVar()
        # self.replace_match_case = tk.BooleanVar()
        self.fields = self.Fields(
            replace_replace_this=(tk.StringVar(), ""),
            replace_replace_with=(tk.StringVar(), ""),
            replace_match_case=(tk.BooleanVar(), False),
        )
        # Replace this, entry
        ttk.Label(self.lf, text="Replace").grid(column=0, row=0, sticky="w")
        self.replace_this_entry = ttk.Entry(
            self.lf, width=10, textvariable=self.fields.replace_replace_this
        )
        self.replace_this_entry.grid(column=1, row=0, sticky="ew")

        # Replace with, entry
        ttk.Label(self.lf, text="With").grid(column=0, row=1, sticky="w")
        self.replace_with_entry = ttk.Entry(
            self.lf, width=10, textvariable=self.fields.replace_replace_with
        )
        self.replace_with_entry.grid(column=1, row=1, sticky="ew")

        # Match case, checkbutton
        self.match_case_check = ttk.Checkbutton(
            self.lf,
            text="Match Case",
            variable=self.fields.replace_match_case,
        )
        self.match_case_check.grid(column=0, row=2)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)

        self.bindEntries()

    def replaceThisGet(self, *args, **kwargs):
        return self.replace_replace_this.get()

    def replaceWithGet(self, *args, **kwargs):
        return self.replace_replace_with.get()

    def matchCaseGet(self, *args, **kwargs):
        return self.replace_match_case.get()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        # Calls to update the new name column
        self.fields.replace_replace_this.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.replace_replace_with.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.replace_match_case.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.replace_replace_this.set("")
    #     self.replace_replace_with.set("")
    #     self.replace_match_case.set(False)

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.replace_replace_this.set(var_dict["replace_replace_this"])
    #     self.replace_replace_with.set(var_dict["replace_replace_with"])
    #     self.replace_match_case.set(var_dict["replace_match_case"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_["replace_replace_this"] = nb.replace.replaceThisGet()
    #     dict_["replace_replace_with"] = nb.replace.replaceWithGet()
    #     dict_["replace_match_case"] = nb.replace.matchCaseGet()


def replace_action(name, **fields_dict):
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
