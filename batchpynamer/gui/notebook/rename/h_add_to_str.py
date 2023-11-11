from tkinter import ttk

from batchpynamer.gui import utils as bpn_gui_utils
from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnBoolVar,
    BpnIntVar,
    BpnStrVar,
)


class AddToStr(BaseNamingWidget, ttk.LabelFrame):  # (7)
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
        self.fields = self.Fields(
            add_to_str_prefix=BpnStrVar(""),
            add_to_str_insert_this=BpnStrVar(""),
            add_to_str_at_pos=BpnIntVar(0),
            add_to_str_suffix=BpnStrVar(""),
            add_to_str_word_space=BpnBoolVar(False),
        )

    def tk_init(self, master):
        super().tk_init(
            master,
            column=4,
            row=0,
            rowspan=2,
            text="Add (7)",
            reset_column_row=(2, 5),
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
            from_=-bpn_gui_utils.drive_max_name_len(),
            to=bpn_gui_utils.drive_max_name_len(),
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

        self.bindings()
