import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class MoveParts(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (6)
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
        pass

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Move Parts (6)")
        self.lf.grid(column=0, row=2, columnspan=3, sticky="nsew")

        # Variable defs
        # self.move_parts_ori_pos = tk.StringVar()
        # self.move_parts_ori_n = tk.IntVar()
        # self.move_parts_end_pos = tk.StringVar()
        # self.move_parts_end_n = tk.IntVar()
        # self.move_parts_sep = tk.StringVar()
        self.fields = self.Fields(
            move_parts_ori_pos=(tk.StringVar(), ("None", "Start", "End")),
            move_parts_ori_n=(tk.IntVar(), 0),
            move_parts_end_pos=(tk.StringVar(), ("Start", "End", "Position")),
            move_parts_end_n=(tk.IntVar(), 0),
            move_parts_sep=(tk.StringVar(), ""),
        )

        # Copy from, combobox
        ttk.Label(self.lf, text="Copy").grid(column=0, row=0)
        self.ori_pos_combo = ttk.Combobox(
            self.lf,
            width=5,
            state="readonly",
            # values=("None", "Start", "End"),
            values=self.fields.move_parts_ori_pos.default,
            textvariable=self.fields.move_parts_ori_pos,
        )
        self.ori_pos_combo.grid(column=1, row=0, sticky="ew")
        self.ori_pos_combo.current(0)

        # Copy n characters, spinbox
        ttk.Label(self.lf, text="Chars.").grid(column=2, row=0)
        self.ori_n_spin = ttk.Spinbox(
            self.lf,
            width=3,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.move_parts_ori_n,
        )
        self.ori_n_spin.grid(column=3, row=0)

        # Paste to, combobox
        ttk.Label(self.lf, text="Paste").grid(column=4, row=0)
        self.end_pos_combo = ttk.Combobox(
            self.lf,
            width=5,
            state="readonly",
            # values=("Start", "End", "Position"),
            values=self.fields.move_parts_end_pos.default,
            textvariable=self.fields.move_parts_end_pos,
        )
        self.end_pos_combo.grid(column=5, row=0, sticky="ew")
        self.end_pos_combo.current(0)

        # Paste in n position, spinbox
        ttk.Label(self.lf, text="Pos.").grid(column=6, row=0)
        self.end_n_spin = ttk.Spinbox(
            self.lf,
            width=3,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.move_parts_end_n,
        )
        self.end_n_spin.grid(column=7, row=0)

        # Separator between pasted part and position, entry
        ttk.Label(self.lf, text="Sep.").grid(column=8, row=0)
        self.sep_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.move_parts_sep
        )
        self.sep_entry.grid(column=9, row=0)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=10, row=1, sticky="w", padx=2, pady=2)

        self.bindEntries()

    # def oriPosGet(self, *args, **kwargs):
    #     return self.move_parts_ori_pos.get()

    # def oriNGet(self, *args, **kwargs):
    #     return self.move_parts_ori_n.get()

    # def endPosGet(self, *args, **kwargs):
    #     return self.move_parts_end_pos.get()

    # def endNGet(self, *args, **kwargs):
    #     return self.move_parts_end_n.get()

    # def sepGet(self, *args, **kwargs):
    #     return self.move_parts_sep.get()

    def bindEntries(self, *args, **kwargs):
        """Defines the binded actions"""
        self.fields.move_parts_ori_n.trace_add("write", self.fromAddTo)
        self.fields.move_parts_end_n.trace_add("write", self.fromAddTo)
        self.ori_pos_combo.bind("<<ComboboxSelected>>", self.defocus)
        self.end_pos_combo.bind("<<ComboboxSelected>>", self.defocus)

        # calls to update the new name column
        self.fields.move_parts_ori_pos.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.move_parts_ori_n.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.move_parts_end_pos.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.move_parts_end_n.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.move_parts_sep.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.ori_pos_combo.selection_clear()
        self.end_pos_combo.selection_clear()

    def fromAddTo(self, *args, **kwargs):
        """
        Checks if the from_n value is bigger than the to_n value,
        If so raises the to_n value accordingly.
        """
        # a = self.oriNGet()
        # b = self.endNGet()
        a = self.fields.move_parts_ori_n.get()
        b = self.fields.move_parts_end_n.get()

        if a > b:
            self.fields.move_parts_end_n.set(a)

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget"""
    #     self.move_parts_ori_pos.set("None")
    #     self.move_parts_ori_n.set(0)
    #     self.move_parts_end_pos.set("Start")
    #     self.move_parts_end_n.set(0)
    #     self.move_parts_sep.set("")

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.move_parts_ori_pos.set(var_dict["move_parts_ori_pos"])
    #     self.move_parts_ori_n.set(var_dict["move_parts_ori_n"])
    #     self.move_parts_end_pos.set(var_dict["move_parts_end_pos"])
    #     self.move_parts_end_n.set(var_dict["move_parts_end_n"])
    #     self.move_parts_sep.set(var_dict["move_parts_sep"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_["move_parts_ori_pos"] = nb.Move_Parts.oriPosGet()
    #     dict_["move_parts_ori_n"] = nb.Move_Parts.oriNGet()
    #     dict_["move_parts_end_pos"] = nb.Move_Parts.endPosGet()
    #     dict_["move_parts_end_n"] = nb.Move_Parts.endNGet()
    #     dict_["move_parts_sep"] = nb.Move_Parts.sepGet()


def move_copy_action(name, **fields_dict):
    """
    Copies and pastes the selected characters to the selected
    position.
    """
    move_parts_ori_pos = fields_dict.get("move_parts_ori_pos")
    move_parts_ori_n = fields_dict.get("move_parts_ori_n")
    move_parts_end_pos = fields_dict.get("move_parts_end_pos")
    move_parts_end_n = fields_dict.get("move_parts_end_n")
    move_parts_sep = fields_dict.get("move_parts_sep")

    if move_parts_ori_pos == "Start":
        if move_parts_end_pos == "End":
            name = (
                name[move_parts_ori_n:]
                + move_parts_sep
                + name[:move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[move_parts_ori_n:move_parts_end_n]
                + move_parts_sep
                + name[:move_parts_ori_n]
                + move_parts_sep
                + name[move_parts_end_n:]
            )

    elif move_parts_ori_pos == "End":
        if move_parts_end_pos == "Start":
            name = (
                name[-move_parts_ori_n:]
                + move_parts_sep
                + name[:-move_parts_ori_n]
            )

        elif move_parts_end_pos == "Position":
            name = (
                name[:move_parts_end_n]
                + move_parts_sep
                + name[-move_parts_ori_n:]
                + move_parts_sep
                + name[move_parts_end_n:-move_parts_ori_n]
            )

    return name
