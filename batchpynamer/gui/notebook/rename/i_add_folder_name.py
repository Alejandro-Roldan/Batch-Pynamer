import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer.gui.basewidgets import (
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
        self.fields = self.Fields(
            add_folder_name_name_pos=BpnComboVar(
                ("Prefix", "Suffix", "Position")
            ),
            add_folder_name_pos=BpnIntVar(0),
            add_folder_name_sep=BpnStrVar(""),
            add_folder_name_levels=BpnIntVar(0),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=3,
            row=2,
            columnspan=2,
            text="Add Folder Name (8)",
        )
        super().tk_init(reset_column_row=(8, 1))

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
