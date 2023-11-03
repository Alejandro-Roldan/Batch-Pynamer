import tkinter as tk

from tkinter import ttk

import batchpynamer
from .. import basewidgets


class AddFolderName(basewidgets.BaseNamingWidget, ttk.LabelFrame):  # (8)
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

    def tk_init(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Append Folder Name (8)")
        self.lf.grid(column=3, row=2, columnspan=2, sticky="nsew")

        # Variable defs
        # self.add_folder_name_name_pos = tk.StringVar()
        # self.add_folder_name_pos = tk.IntVar()
        # self.add_folder_name_sep = tk.StringVar()
        # self.add_folder_name_levels = tk.IntVar()
        self.fields = self.Fields(
            add_folder_name_name_pos=(
                tk.StringVar(),
                ("Prefix", "Suffix", "Position"),
            ),
            add_folder_name_pos=(tk.IntVar(), 0),
            add_folder_name_sep=(tk.StringVar(), ""),
            add_folder_name_levels=(tk.IntVar(), 0),
        )

        # Name, combobox
        ttk.Label(self.lf, text="Name").grid(column=0, row=0, sticky="ew")
        self.name_pos_combo = ttk.Combobox(
            self.lf,
            width=5,
            state="readonly",
            # values=("Prefix", "Suffix", "Position"),
            values=self.fields.add_folder_name_name_pos.default,
            textvariable=self.fields.add_folder_name_name_pos,
        )
        self.name_pos_combo.grid(column=1, row=0, sticky="ew")
        self.name_pos_combo.current(0)

        # Folders add_folder_name_levels, spinbox
        ttk.Label(self.lf, text="Pos.").grid(column=2, row=0, sticky="ew")
        self.levels_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=-batchpynamer.MAX_NAME_LEN,
            to=batchpynamer.MAX_NAME_LEN,
            textvariable=self.fields.add_folder_name_pos,
        )
        self.levels_spin.grid(column=3, row=0)

        # Separator, entry
        ttk.Label(self.lf, text="Sep.").grid(column=4, row=0, sticky="ew")
        self.sep_entry = ttk.Entry(
            self.lf, width=5, textvariable=self.fields.add_folder_name_sep
        )
        self.sep_entry.grid(column=5, row=0, sticky="ew")

        # Folders add_folder_name_levels, spinbox
        ttk.Label(self.lf, text="Levels").grid(column=6, row=0, sticky="ew")
        self.levels_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=0,
            to=500,
            textvariable=self.fields.add_folder_name_levels,
        )
        self.levels_spin.grid(column=7, row=0)

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=20, row=20, sticky="w", padx=2, pady=2)

        self.bindEntries()

    # def namePosGet(self, *args, **kwargs):
    #     return self.add_folder_name_name_pos.get()

    # def posGet(self, *args, **kwargs):
    #     return self.add_folder_name_pos.get()

    # def sepGet(self, *args, **kwargs):
    #     return self.add_folder_name_sep.get()

    # def levelsGet(self, *args, **kwargs):
    #     return self.add_folder_name_levels.get()

    def bindEntries(self, *args, **kwargs):
        """What to execute when the bindings happen."""
        # Defocus the hightlight when changing combobox
        self.name_pos_combo.bind("<<ComboboxSelected>>", self.defocus)

        # Calls to update the new name column
        self.fields.add_folder_name_name_pos.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_folder_name_pos.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_folder_name_sep.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )
        self.fields.add_folder_name_levels.trace_add(
            "write", batchpynamer.fn_treeview.showNewName
        )

    def defocus(self, *args, **kwargs):
        """
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        """
        self.name_pos_combo.selection_clear()

    # def resetWidget(self, *args, **kwargs):
    #     """Resets each and all data variables inside the widget."""
    #     self.add_folder_name_name_pos.set("Prefix")
    #     self.add_folder_name_pos.set(0)
    #     self.add_folder_name_sep.set("")
    #     self.add_folder_name_levels.set(0)

    # def setCommand(self, var_dict, *args, **kwargs):
    #     """
    #     Sets the variable fields according to the loaded
    #     command dictionary
    #     """
    #     self.add_folder_name_name_pos.set(var_dict["append_folder_name_name_pos"])
    #     self.add_folder_name_sep.set(var_dict["append_folder_name_pos"])
    #     self.add_folder_name_sep.set(var_dict["append_folder_name_sep"])
    #     self.add_folder_name_levels.set(var_dict["append_folder_name_levels"])

    # @staticmethod
    # def appendVarValToDict(dict_={}, *args, **kwargs):
    #     dict_[
    #         "append_folder_name_name_pos"
    #     ] = nb.append_folder_name.namePosGet()
    #     dict_["append_folder_name_pos"] = nb.append_folder_name.posGet()
    #     dict_["append_folder_name_sep"] = nb.append_folder_name.sepGet()
    #     dict_["append_folder_name_levels"] = nb.append_folder_name.levelsGet()


def add_folder_rename(name, path, **fields_dict):
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
