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

    def tk_init(self, master):
        super().__init__(
            master,
            column=4,
            row=0,
            rowspan=2,
            text="Add (7)",
        )
        super().tk_init(reset_column_row=(2, 5))

        # Variable defs
        self.fields = self.Fields(
            add_to_str_prefix=(tk.StringVar(), ""),
            add_to_str_insert_this=(tk.StringVar(), ""),
            add_to_str_at_pos=(tk.IntVar(), 0),
            add_to_str_suffix=(tk.StringVar(), ""),
            add_to_str_word_space=(tk.BooleanVar(), False),
        )

        # Prefix, entry
        ttk.Label(self, text="Prefix").grid(column=0, row=0, sticky="ew")
        self.prefix_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.add_to_str_prefix,
        )
        self.prefix_entry.grid(column=1, row=0, sticky="ew")

        # Insert, entry
        ttk.Label(self, text="Insert").grid(column=0, row=1, sticky="ew")
        self.insert_this_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.add_to_str_insert_this,
        )
        self.insert_this_entry.grid(column=1, row=1, sticky="ew")

        # Insert char(s) at position, spinbox
        ttk.Label(self, text="At pos.").grid(column=0, row=2, sticky="ew")
        self.at_pos_spin = ttk.Spinbox(
            self,
            width=3,
            from_=-batchpynamer.MAX_NAME_LEN,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.add_to_str_at_pos,
        )
        self.at_pos_spin.grid(column=1, row=2)

        # Suffix, entry
        ttk.Label(self, text="Suffix").grid(column=0, row=3, sticky="ew")
        self.suffix_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.add_to_str_suffix,
        )
        self.suffix_entry.grid(column=1, row=3, sticky="ew")

        # Word space, checkbutton
        self.word_space_check = ttk.Checkbutton(
            self,
            text="Word Space",
            variable=self.fields.add_to_str_word_space,
        )
        self.word_space_check.grid(column=0, row=4)

        self.bindEntries()

    def bindEntries(self):
        """What to execute when the bindings happen."""
        super().bindEntries()
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


def add_rename(name, fields_dict):
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
