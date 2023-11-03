import string
import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class Numbering(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (9)
    """
    Draws the numbering widget. Inside the rename notebook. 9th thing
    to change.
    It has:
        - Dropdown that lets you shoose position
        - ttk.Spinbox to choose at what place in the middle of the name
        - ttk.Spinbox to choose from what number to start numbering
        - ttk.Spinbox to choose the numbering step
        - ttk.Spinbox for how many 0 to use
        - Entry for a separator
        - Dropdown to choose the type of numbering
            - Base 10
            - Base 2
            - Base 8
            - Base 16
            - Uppercase letters
            - Lowercase letter
    """

    def __init__(self):
        pass

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Numbering (9)")
        self.lf.grid(column=5, row=0, rowspan=2, sticky="nsew")

        # Variable defs
        # self.numbering_mode = tk.StringVar()
        # self.numbering_at_n = tk.IntVar()
        # self.numbering_start_num = tk.IntVar()
        # self.numbering_incr_num = tk.IntVar(value=1)
        # self.numbering_pad = tk.IntVar(value=1)
        # self.numbering_sep = tk.StringVar()
        # self.numbering_type_base = tk.StringVar()
        self.fields = self.Fields(
            numbering_mode=(
                tk.StringVar(),
                ("None", "Prefix", "Suffix", "Both", "Position"),
            ),
            numbering_at_n=(tk.IntVar(), 0),
            numbering_start_num=(tk.IntVar(), 0),
            numbering_incr_num=(tk.IntVar(value=1), 1),
            numbering_pad=(tk.IntVar(value=1), 1),
            numbering_sep=(tk.StringVar(), ""),
            numbering_type_base=(
                tk.StringVar(),
                (
                    "Base 10",
                    "Base 2",
                    "Base 8",
                    "Base 16",
                    "Upper Case Letters",
                    "Lower Case Letters",
                ),
            ),
        )

        # Mode, combobox
        ttk.Label(self.lf, text="Mode").grid(column=0, row=0, sticky="ew")
        self.mode_combo = ttk.Combobox(
            self.lf,
            width=5,
            state="readonly",
            # values=("None", "Prefix", "Suffix", "Both", "Position"),
            values=self.fields.numbering_mode.default,
            textvariable=self.fields.numbering_mode,
        )
        self.mode_combo.grid(column=1, row=0, sticky="ew")
        self.mode_combo.current(0)

        # At position, spinbox
        ttk.Label(self.lf, text="At").grid(column=2, row=0, sticky="ew")
        self.at_n_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=-batchpynamer.MAX_NAME_LEN,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.numbering_at_n,
        )
        self.at_n_spin.grid(column=3, row=0)

        # Start from this number, spinbox
        ttk.Label(self.lf, text="Start").grid(column=0, row=1, sticky="ew")
        self.start_num_spin = ttk.Spinbox(
            self.lf,
            width=3,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.numbering_start_num,
        )
        self.start_num_spin.grid(column=1, row=1)

        # Step, spinbox
        ttk.Label(self.lf, text="Incr.").grid(column=2, row=1, sticky="ew")
        self.incr_num_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=1,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.numbering_incr_num,
        )
        self.incr_num_spin.grid(column=3, row=1)
        # TKINTER BUG
        # The ttk.spinbox doesn't begin in the minimun value thats set
        # Solution would be to set it to the desired number as initialization
        # But this is not a bug from my end

        # Padding of possible 0s, spinbox
        ttk.Label(self.lf, text="Pad.").grid(column=0, row=2, sticky="ew")
        self.pad_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=1,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.numbering_pad,
        )
        self.pad_spin.grid(column=1, row=2)
        # TKINTER BUG
        # The ttk.spinbox doesn't begin in the minimun value thats set
        # Solution would be to set it to the desired number as initialization
        # But this is not a bug from my end

        # Separator, entry
        ttk.Label(self.lf, text="Sep.").grid(column=2, row=2, sticky="ew")
        self.sep_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.numbering_sep
        )
        self.sep_entry.grid(column=3, row=2, sticky="ew")

        # Type of enumeration/Base, combobox
        ttk.Label(self.lf, text="Type").grid(column=0, row=3, sticky="w")
        self.type_base_combo = ttk.Combobox(
            self.lf,
            width=5,
            state="readonly",
            values=self.fields.numbering_type_base.default,
            textvariable=self.fields.numbering_type_base,
        )
        self.type_base_combo.grid(column=1, row=3, columnspan=3, sticky="ew")
        # self.type_base_combo["value"] = (
        #     "Base 10",
        #     "Base 2",
        #     "Base 8",
        #     "Base 16",
        #     "Upper Case Letters",
        #     "Lower Case Letters",
        # )
        self.type_base_combo.current(0)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=20, row=20, sticky="w", padx=2, pady=2)

        self.bindEntries()

    # def modeGet(self, *args, **kwargs):
    #     return self.numbering_mode.get()

    # def atNGet(self, *args, **kwargs):
    #     return self.numbering_at_n.get()

    # def startNumGet(self, *args, **kwargs):
    #     return self.numbering_start_num.get()

    # def incrNumGet(self, *args, **kwargs):
    #     return self.numbering_incr_num.get()

    # def padGet(self, *args, **kwargs):
    #     return self.numbering_pad.get()

    # def sepGet(self, *args, **kwargs):
    #     return self.numbering_sep.get()

    # def typeBaseGet(self, *args, **kwargs):
    #     return self.numbering_type_base.get()

    def bindEntries(self, *args, **kwargs):
        """What to execute when the bindings happen."""
        # defocus the hightlight when changing combobox
        self.mode_combo.bind("<<ComboboxSelected>>", self.defocus)
        self.type_base_combo.bind("<<ComboboxSelected>>", self.defocus)

        # calls to update the new name column
        self.fields.numbering_mode.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_at_n.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_start_num.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_incr_num.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_pad.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_sep.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.numbering_type_base.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.mode_combo.selection_clear()
        self.type_base_combo.selection_clear()

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget."""
    #     self.numbering_mode.set("None")
    #     self.numbering_at_n.set(0)
    #     self.numbering_start_num.set(0)
    #     self.numbering_incr_num.set(1)
    #     self.numbering_pad.set(1)
    #     self.numbering_sep.set("")
    #     self.numbering_type_base.set("Base 10")

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.numbering_mode.set(var_dict["numbering_mode"])
    #     self.numbering_at_n.set(var_dict["numbering_at_n"])
    #     self.numbering_start_num.set(var_dict["numbering_start_num"])
    #     self.numbering_incr_num.set(var_dict["numbering_incr_num"])
    #     self.numbering_pad.set(var_dict["numbering_pad"])
    #     self.numbering_sep.set(var_dict["numbering_sep"])
    #     self.numbering_type_base.set(var_dict["numbering_type_base"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_["numbering_mode"] = nb.numbering.modeGet()
    #     dict_["numbering_at_n"] = nb.numbering.atNGet()
    #     dict_["numbering_start_num"] = nb.numbering.startNumGet()
    #     dict_["numbering_incr_num"] = nb.numbering.incrNumGet()
    #     dict_["numbering_pad"] = nb.numbering.padGet()
    #     dict_["numbering_sep"] = nb.numbering.sepGet()
    #     dict_["numbering_type_base"] = nb.numbering.typeBaseGet()


def numbering_rename(name, idx, **fields_dict):
    """Calls to create the numbering and then sets it up inplace"""
    numbering_mode = fields_dict.get("numbering_mode")
    numbering_at_n = fields_dict.get("numbering_at_n")
    numbering_start_num = fields_dict.get("numbering_start_num")
    numbering_incr_num = fields_dict.get("numbering_incr_num")
    numbering_sep = fields_dict.get("numbering_sep")
    numbering_type_base = fields_dict.get("numbering_type_base")
    numbering_pad = fields_dict.get("numbering_pad")

    # Calculate what number we are in taking into account the step and
    # the starting number
    n = idx + numbering_start_num + (numbering_incr_num - 1) * idx
    # Change the number to string and whatever base we selected
    n = numbering_create(n, numbering_type_base, numbering_pad)

    if numbering_mode == "Prefix":
        name = n + numbering_sep + name
    elif numbering_mode == "Suffix":
        name = name + numbering_sep + n
    elif numbering_mode == "Both":
        name = n + numbering_sep + name + numbering_sep + n
    elif numbering_mode == "Position":
        # If blocks to determine where to write the separators and how to
        # act depending on where we have to write it to make it seem
        # seamless
        if numbering_at_n == 0:
            name = n + numbering_sep + name
        elif numbering_at_n == -1 or numbering_at_n >= len(name):
            name = name + numbering_sep + n
        elif numbering_at_n > 0:
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )
        elif numbering_at_n < -1:
            numbering_at_n += 1
            name = (
                name[:numbering_at_n]
                + numbering_sep
                + n
                + numbering_sep
                + name[numbering_at_n:]
            )

    return name


def numbering_create(n, type_base, pad):
    """
    Changes the number to the the chosen base, removes the part of the
    string that specifies that its a number in such a base and then
    adds the padding 0s.
    For the letter cases transforms the number to what letter it would
    correspond and adds the padding As
    """
    # Number cases
    if type_base == "Base 10":
        n = str(n)
        n = n.rjust(pad, "0")
    elif type_base == "Base 2":
        n = bin(n)
        n = n[2:]
        n = n.rjust(pad, "0")
    elif type_base == "Base 8":
        n = oct(n)
        n = n[2:]
        n = n.rjust(pad, "0")
    elif type_base == "Base 16":
        n = hex(n)
        n = n[2:]
        n = n.rjust(pad, "0")

    # Letter cases
    else:
        # Uses a cycle variable to know how many times it has to loop
        # ex: 1 -> A, 27 -> AA, 53 -> BA
        cycle = n // 26
        letter_n = ""
        for a in range(0, cycle + 1):
            letter_n = letter_n + string.ascii_lowercase[n - 26 * cycle]
        n = letter_n.rjust(pad, "a")

        if type_base == "Upper Case Letters":
            n = n.upper()

    return n
