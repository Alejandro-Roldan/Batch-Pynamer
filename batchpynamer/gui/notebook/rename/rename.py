import logging
import os
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
import batchpynamer.data as bpn_data
import batchpynamer.gui as bpn_gui
from batchpynamer.data.rename_data_tools import (
    rename_create_new_name_action,
    rename_system_rename,
)
from batchpynamer.gui import basewidgets, commands, infobar
from batchpynamer.gui.trees import trees


class LastRename:
    """
    A last rename object that saves the previous renames and
    gives the ability to undo the changes

    A list of tuples where tuple[0] is the old name and
    tuple[1] the new name
    """

    def __init__(self):
        self.last_rename_list = []

    def pair_append(self, old_path, new_path):
        """Appending new items"""
        pair_tuple = (old_path, new_path)
        self.last_rename_list.append(pair_tuple)

        return pair_tuple

    def get(self):
        """Return the last rename array"""
        return self.last_rename_list

    def last_name_list_get(self):
        """Return the old name in the last rename"""
        last_name_list = list(
            last_name[0] for last_name in self.last_rename_list
        )
        return last_name_list

    def new_name_list_get(self):
        """Return the selected new name in the last rename"""
        new_name_list = list(new_name[1] for new_name in self.last_rename_list)
        return new_name_list

    def clear(self):
        """Clear the last rename array"""
        self.last_rename_list = []

    def __str__(self):
        """Define how to print the object"""
        return str(self.last_rename_list)


class Rename(basewidgets.BaseWidget, ttk.Frame):
    """
    Draws the Rename button. Inside rename notebook. This is always last.
    It has:
        - Button that calls to permanently rename the selected files
        - Button that resets all fields inside the rename notebook
        - Button that reverts the last renaming action
    """

    def __init__(self, master):
        super().__init__(master, column=1, row=0, sticky="w" + "e")

        self.load_command_button = ttk.Button(
            self,
            text="Command",
            command=commands.command_gui_apply_action,
        )
        self.load_command_button.grid(
            column=0, row=1, padx=1, pady=1, sticky="e"
        )
        # Disable the button if no path to where commands are stored
        # TODO add also disable if no command selected
        if not bpn.CONFIG_FOLDER_PATH:
            self.load_command_button.config(state="disable")

        self.reset_button = ttk.Button(
            self,
            text="Reset",
            command=rename_gui_all_fields_reset,
        )
        self.reset_button.grid(column=1, row=0, padx=1, pady=1, sticky="e")

        self.revert_button = ttk.Button(
            self,
            text="Undo",
            command=rename_gui_undo_rename_call,
        )
        self.revert_button.grid(column=1, row=1, padx=1, pady=1, sticky="e")

        self.rename_button = ttk.Button(
            self,
            text="Rename",
            command=rename_gui_apply_rename_call,
        )
        self.rename_button.grid(
            column=2, row=0, rowspan=2, padx=1, pady=1, sticky="nse"
        )


def rename_gui_undo_rename_call(event=None):
    """Undo the last name changes.

    You can only undo 1 step back.
    """
    # Get a copy of the last changes list so when it gets modified it
    # doesnt affect this one and gets stuck in an infinite loop changing
    # back and forth
    # Undo the changes starting with the last one and going up
    last_rename_list = reversed(bpn_gui.last_rename.get())

    # Try to undo the changes only if there are changes to undo
    if last_rename_list:
        # Show that it's in the process
        infobar.show_working()

        logging.info("Undo:")
        for name_pair in last_rename_list:
            # Get the new path and the old path from the last
            # changes paths pairs
            new_path = name_pair[1]
            last_path = name_pair[0]

            # Apply a system rename
            rename_system_rename(new_path, last_path)
        logging.info("-" * 20)

        # Update the folders treeviews
        trees.refresh_treeviews()

        infobar.finish_show_working(inf_msg="Finished Undo Operation")

        # Clear the last rename list pairs
        bpn_gui.last_rename.clear()

    # Else show msg
    else:
        bpn_gui.info_bar.last_action_set("No Changes to Undo")


def rename_gui_apply_rename_call(event=None):
    """GUI rename selected items"""
    # Clear the last_rename action list
    bpn_gui.last_rename.clear()
    # Get selected items
    selection = list(bpn_gui.fn_treeview.selection_get())

    # When to reverse the naming items list so as to skip naming problems
    # like with recursiveness naming a folder before the files in it so
    # then the files can't be renamed because the path pointer doesn't
    # exists. Optimized the boolean function
    # A=menu_bar.rename_order_bottom_to_top.get()
    # B=nb.filters.depthGet()
    # C=nb.filters.reverseGet()
    # F(A,B,C)=~BA+B~C
    if (
        not bpn_gui.filters_widget.fields.depth.get()
        and bpn_gui.menu_bar.rename_order_bottom_to_top.get()
    ) or (
        bpn_gui.filters_widget.fields.depth.get()
        and not bpn_gui.filters_widget.fields.reverse.get()
    ):
        selection = reversed(selection)

    # Try to apply the changes only if there is a selection
    if selection:
        # Show that its in the process
        infobar.show_working()

        logging.info("Rename:")
        for old_path in selection:
            directory, slash, old_name = old_path.rpartition("/")
            name = bpn_gui.fn_treeview.tree_folder.set(old_path, "#1")
            new_path = directory + slash + name

            # Rename and handle output
            result = rename_system_rename(old_path, new_path)
            if result is None:
                bpn_gui.last_rename.pair_append(old_path, new_path)
            else:
                basewidgets.ErrorFrame(error_desc=result)
        logging.info("-" * 20)

        trees.refresh_treeviews()

        # Show that its finish
        infobar.finish_show_working(inf_msg="Finished Rename")

    # Else show a msg that there is no selection
    else:
        bpn_gui.info_bar.last_action_set("No Selected Items")


def rename_gui_all_fields_reset(event=None):
    """Calls all resetWidget Methods"""
    bpn_gui.rename_from_file.resetWidget()
    bpn_gui.rename_from_reg_exp.resetWidget()
    bpn_gui.name_basic.resetWidget()
    bpn_gui.replace.resetWidget()
    bpn_gui.case.resetWidget()
    bpn_gui.remove.resetWidget()
    bpn_gui.move_parts.resetWidget()
    bpn_gui.add_to_str.resetWidget()
    bpn_gui.add_folder_name.resetWidget()
    bpn_gui.numbering.resetWidget()
    bpn_gui.ext_replace.resetWidget()

    bpn_gui.info_bar.last_action_set("Full Reset")


def rename_gui_all_fields_get():
    return {
        # GUI fields
        **bpn_gui.rename_from_file.fields.get_all(),
        **bpn_gui.rename_from_reg_exp.fields.get_all(),
        **bpn_gui.name_basic.fields.get_all(),
        **bpn_gui.replace.fields.get_all(),
        **bpn_gui.case.fields.get_all(),
        **bpn_gui.remove.fields.get_all(),
        **bpn_gui.move_parts.fields.get_all(),
        **bpn_gui.add_to_str.fields.get_all(),
        **bpn_gui.add_folder_name.fields.get_all(),
        **bpn_gui.numbering.fields.get_all(),
        **bpn_gui.ext_replace.fields.get_all(),
    }


def rename_gui_create_new_name_action(name, idx, path):
    return rename_create_new_name_action(
        name, idx, path, **rename_gui_all_fields_get()
    )
