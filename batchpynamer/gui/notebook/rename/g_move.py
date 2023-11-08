from tkinter import ttk

from batchpynamer.gui import utils as bpn_gui_utils
from batchpynamer.gui.basewidgets import (
    BaseNamingWidget,
    BpnComboVar,
    BpnIntVar,
    BpnStrVar,
)
from batchpynamer.gui.notebook.rename.utils import spin_box_lower_limit_update


class MoveParts(BaseNamingWidget, ttk.LabelFrame):  # (6)
    """
    Draws the move/copy parts widget. Inside rename notebook.
    6th thing to change.
    It has:
        - Combobox to select where to select the text from (start, end)
        - ttk.Spinbox to select how many characters to select
        - Combobox to select where to paste the char(s) to
        (start, end, position)
        - ttk.Spinbox to select where to paste when 'position' is selected
        - Entry to write a separator
    """

    def __init__(self):
        self.fields = self.Fields(
            move_parts_ori_pos=BpnComboVar(("None", "Start", "End")),
            move_parts_ori_n=BpnIntVar(0),
            move_parts_end_pos=BpnComboVar(("Start", "End", "Position")),
            move_parts_end_n=BpnIntVar(0),
            move_parts_sep=BpnStrVar(""),
        )

    def tk_init(self, master):
        super().__init__(
            master,
            column=0,
            row=2,
            columnspan=3,
            text="Move Parts (6)",
        )
        super().tk_init(reset_column_row=(10, 1))

        # Copy from, combobox
        ttk.Label(self, text="Copy").grid(column=0, row=0)
        self.ori_pos_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.move_parts_ori_pos.options,
            textvariable=self.fields.move_parts_ori_pos,
        )
        self.ori_pos_combo.grid(column=1, row=0, sticky="ew")

        # Copy n characters, spinbox
        ttk.Label(self, text="Chars.").grid(column=2, row=0)
        self.ori_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.move_parts_ori_n,
        )
        self.ori_n_spin.grid(column=3, row=0)

        # Paste to, combobox
        ttk.Label(self, text="Paste").grid(column=4, row=0)
        self.end_pos_combo = ttk.Combobox(
            self,
            width=5,
            state="readonly",
            values=self.fields.move_parts_end_pos.options,
            textvariable=self.fields.move_parts_end_pos,
        )
        self.end_pos_combo.grid(column=5, row=0, sticky="ew")

        # Paste in n position, spinbox
        ttk.Label(self, text="Pos.").grid(column=6, row=0)
        self.end_n_spin = ttk.Spinbox(
            self,
            width=3,
            to=bpn_gui_utils.drive_max_name_len(),
            textvariable=self.fields.move_parts_end_n,
        )
        self.end_n_spin.grid(column=7, row=0)

        # Separator between pasted part and position, entry
        ttk.Label(self, text="Sep.").grid(column=8, row=0)
        self.sep_entry = ttk.Entry(
            self, width=5, textvariable=self.fields.move_parts_sep
        )
        self.sep_entry.grid(column=9, row=0)

        self.bindings()

    def bindings(self):
        """Defines the binded actions"""
        super().bindings()

        self.fields.move_parts_ori_n.trace_add("write", self.limit_end_n)
        self.fields.move_parts_end_n.trace_add("write", self.limit_end_n)

    def limit_end_n(self, var=None, index=None, mode=None):
        """Limits move_parts_end_n (b) with move_parts_ori_n (a)"""
        spin_box_lower_limit_update(
            self.fields.move_parts_ori_n, self.fields.move_parts_end_n
        )
