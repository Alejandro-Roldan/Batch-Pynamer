import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class AddToStr(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (7)
    """
    Draws the Add widget. Inside the rename notebook. 7th thing to change.
    It has:
        - A prefix entry that adds the char(s) as a prefix
        - An insert entry that at adds the char(s) at the specified pos
        - A at pos spinbox that specifies the position to insert
        the char(s)
        - A suffix entry that adds the char(s) as a suffix
        - A word space checkbox that adds a space before each capital
        letter
    """

    def __init__(self):
        pass

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Add (7)")
        self.lf.grid(column=4, row=0, rowspan=2, sticky="nsew")

        # Variable defs
        # self.add_to_str_prefix = tk.StringVar()
        # self.add_to_str_insert_this = tk.StringVar()
        # self.add_to_str_at_pos = tk.IntVar()
        # self.add_to_str_suffix = tk.StringVar()
        # self.add_to_str_word_space = tk.BooleanVar()
        self.fields = self.Fields(
            add_to_str_prefix=(tk.StringVar(), ""),
            add_to_str_insert_this=(tk.StringVar(), ""),
            add_to_str_at_pos=(tk.IntVar(), 0),
            add_to_str_suffix=(tk.StringVar(), ""),
            add_to_str_word_space=(tk.BooleanVar(), False),
        )

        # Prefix, entry
        ttk.Label(self.lf, text="Prefix").grid(column=0, row=0, sticky="ew")
        self.prefix_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.add_to_str_prefix
        )
        self.prefix_entry.grid(column=1, row=0, sticky="ew")

        # Insert, entry
        ttk.Label(self.lf, text="Insert").grid(column=0, row=1, sticky="ew")
        self.insert_this_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.add_to_str_insert_this
        )
        self.insert_this_entry.grid(column=1, row=1, sticky="ew")

        # Insert char(s) at position, spinbox
        ttk.Label(self.lf, text="At pos.").grid(column=0, row=2, sticky="ew")
        self.at_pos_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=-batchpynamer.MAX_NAME_LEN,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.add_to_str_at_pos,
        )
        self.at_pos_spin.grid(column=1, row=2)
        # self.fields.add_to_str_at_pos.set(0)

        # Suffix, entry
        ttk.Label(self.lf, text="Suffix").grid(column=0, row=3, sticky="ew")
        self.suffix_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.add_to_str_suffix
        )
        self.suffix_entry.grid(column=1, row=3, sticky="ew")

        # Word space, checkbutton
        self.word_space_check = ttk.Checkbutton(
            self.lf,
            text="Word Space",
            variable=self.fields.add_to_str_word_space,
        )
        self.word_space_check.grid(column=0, row=4)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=20, row=20, sticky="w", padx=2, pady=2)

        self.bindEntries()

    # def prefixGet(self, *args, **kwargs):
    #     return self.add_to_str_prefix.get()

    # def insertThisGet(self, *args, **kwargs):
    #     return self.add_to_str_insert_this.get()

    # def atPosGet(self, *args, **kwargs):
    #     return self.add_to_str_at_pos.get()

    # def suffixGet(self, *args, **kwargs):
    #     return self.add_to_str_suffix.get()

    # def wordSpaceGet(self, *args, **kwargs):
    #     return self.add_to_str_word_space.get()

    def bindEntries(self, *args, **kwargs):
        """What to execute when the bindings happen."""
        # calls to update the new name column
        self.fields.add_to_str_prefix.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_to_str_insert_this.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_to_str_at_pos.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_to_str_suffix.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_to_str_word_space.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget."""
    #     self.add_to_str_prefix.set("")
    #     self.add_to_str_insert_this.set("")
    #     self.add_to_str_at_pos.set(0)
    #     self.add_to_str_suffix.set("")
    #     self.add_to_str_word_space.set(False)

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.add_to_str_prefix.set(var_dict["add_to_string_prefix"])
    #     self.add_to_str_insert_this.set(var_dict["add_to_string_insert_this"])
    #     self.add_to_str_at_pos.set(var_dict["add_to_string_at_pos"])
    #     self.add_to_str_suffix.set(var_dict["add_to_string_suffix"])
    #     self.add_to_str_word_space.set(var_dict["add_to_string_word_space"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_["add_to_string_prefix"] = nb.add_to_string.prefixGet()
    #     dict_["add_to_string_insert_this"] = nb.add_to_string.insertThisGet()
    #     dict_["add_to_string_at_pos"] = nb.add_to_string.atPosGet()
    #     dict_["add_to_string_suffix"] = nb.add_to_string.suffixGet()
    #     dict_["add_to_string_word_space"] = nb.add_to_string.wordSpaceGet()


def add_rename(name, **fields_dict):
    """
    Adds the char(s) to the specified position.
    Also can add spaces before capital letters.
    """
    add_to_str_prefix = fields_dict.get("add_to_str_prefix")
    add_to_str_insert_this = fields_dict.get("add_to_str_insert_this")
    add_to_str_at_pos = fields_dict.get("add_to_str_at_pos")
    add_to_str_suffix = fields_dict.get("add_to_str_suffix")
    add_to_str_word_space = fields_dict.get("add_to_str_word_space")

    # Add prefix
    name = add_to_str_prefix + name

    # If blocks to determine where to write the sub str
    # To be able to do it seamlessly it needs different ways to act
    # depending on the position
    if add_to_str_at_pos == 0:
        name = add_to_str_insert_this + name
    elif add_to_str_at_pos == -1 or add_to_str_at_pos >= len(name):
        name = name + add_to_str_insert_this
    elif add_to_str_at_pos > 0:
        name = (
            name[:add_to_str_at_pos]
            + add_to_str_insert_this
            + name[add_to_str_at_pos:]
        )
    elif add_to_str_at_pos < -1:
        add_to_str_at_pos += 1
        name = (
            name[:add_to_str_at_pos]
            + add_to_str_insert_this
            + name[add_to_str_at_pos:]
        )

    # Add suffix
    name = name + add_to_str_suffix

    if add_to_str_word_space:  # add a space before each capital letter
        name = "".join([" " + ch if ch.isupper() else ch for ch in name])

    return name
