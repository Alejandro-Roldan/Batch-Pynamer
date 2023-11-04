import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.basewidgets import (
    BaseNamingWidget,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)


class AddFolderName(BaseNamingWidget, ttk.LabelFrame):  # (8)
    """
    Draws the Append Folder Name. Inside the rename notebook. 8th thing to
    change.
    It has:
        - Dropdown that lets you choose position
        - Entry that lets you specify a separator
        - ttk.Spinbox that lets you choose how many folder levels to add
    """

    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(
            master,
            column=3,
            row=2,
            columnspan=2,
            text="Add Folder Name (8)",
        )
        super().tk_init(reset_column_row=(8, 1))

        # Variable defs
        self.fields = self.Fields(
            add_folder_name_name_pos=BpnComboVar(
                ("Prefix", "Suffix", "Position")
            ),
            add_folder_name_pos=BpnIntVar(0),
            add_folder_name_sep=BpnStrVar(""),
            add_folder_name_levels=BpnIntVar(0),
        )

        # Name, combobox
        ttk.Label(self, text="Name").grid(column=0, row=0, sticky="ew")
        self.name_pos_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.add_folder_name_name_pos.options,
            textvariable=self.fields.add_folder_name_name_pos,
        )
        self.name_pos_combo.grid(column=1, row=0, sticky="ew")

        # Folders add_folder_name_levels, spinbox
        ttk.Label(self, text="Pos.").grid(column=2, row=0, sticky="ew")
        self.levels_spin = ttk.Spinbox(
            self,
            width=3,
            from_=-bpn.MAX_NAME_LEN,
            to=bpn.MAX_NAME_LEN,
            textvariable=self.fields.add_folder_name_pos,
        )
        self.levels_spin.grid(column=3, row=0)

        # Separator, entry
        ttk.Label(self, text="Sep.").grid(column=4, row=0, sticky="ew")
        self.sep_entry = ttk.Entry(
            self,
            width=5,
            textvariable=self.fields.add_folder_name_sep,
        )
        self.sep_entry.grid(column=5, row=0, sticky="ew")

        # Folders add_folder_name_levels, spinbox
        ttk.Label(self, text="Levels").grid(column=6, row=0, sticky="ew")
        self.levels_spin = ttk.Spinbox(
            self,
            width=3,
            from_=0,
            to=500,
            textvariable=self.fields.add_folder_name_levels,
        )
        self.levels_spin.grid(column=7, row=0)

        self.bindings()


def add_folder_rename(name, path, fields_dict):
    add_folder_name_name_pos = fields_dict.get("add_folder_name_name_pos")
    add_folder_name_sep = fields_dict.get("add_folder_name_sep")
    add_folder_name_levels = fields_dict.get("add_folder_name_levels")

    # Active when the level is at least 1
    if add_folder_name_levels > 0:
        # Split the directory into a list with each folder
        folders = path.split("/")
        # Initilize the full folder name
        folder_full = ""
        # Loop for each directory level, start at 2 to skip an empty level
        # and the active level (the item itself)
        for i in range(2, add_folder_name_levels + 2):
            # Error handling for setting a level higher than folders are
            try:
                folder_full = folders[-i] + add_folder_name_sep + folder_full
            except IndexError:
                pass

        if add_folder_name_name_pos == "Prefix":
            name = folder_full + name
        elif add_folder_name_name_pos == "Suffix":
            name = name + add_folder_name_sep + folder_full
            # Remove the extra trailing separator
            if add_folder_name_sep:
                name = name[: -len(add_folder_name_sep)]
        elif add_folder_name_name_pos == "Position":
            add_folder_name_pos = fields_dict.get("add_folder_name_pos")
            # If blocks to determine where to write the sub str
            # To be able to do it seamlessly it needs different ways to act
            # depending on the position
            if add_folder_name_pos == 0:
                name = folder_full + name
            elif add_folder_name_pos == -1 or add_folder_name_pos >= len(name):
                name = name + add_folder_name_sep + folder_full
                # Remove the extra trailing separator
                if add_folder_name_sep:
                    name = name[: -len(add_folder_name_sep)]
            elif add_folder_name_pos > 0:
                name = (
                    name[:add_folder_name_pos]
                    + add_folder_name_sep
                    + folder_full
                    + name[add_folder_name_pos:]
                )
            elif add_folder_name_pos < -1:
                add_folder_name_pos += 1
                name = (
                    name[:add_folder_name_pos]
                    + add_folder_name_sep
                    + folder_full
                    + name[add_folder_name_pos:]
                )

    return name
