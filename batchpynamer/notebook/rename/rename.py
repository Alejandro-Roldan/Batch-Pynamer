import os
import tkinter as tk
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer import basewidgets, commands, info_bar

# Cant import files with numbers directly so use
# Equivalent to "import ... as ..."
# name_basic = __import__("", ["02_name_basic"])
from batchpynamer.notebook.rename import (
    a_from_file,
    b_reg_exp,
    c_name_basic,
    d_replace,
    e_case,
    f_remove,
    g_move,
    h_add_to_str,
    i_add_folder_name,
    j_numbering,
    k_ext_replace,
)
from batchpynamer.notebook.rename.utils import new_naming
from batchpynamer.trees import trees

order = [
    "from_file",
    "reg_exp",
    "name_basic",
    "replace",
    "case",
    "remove",
    "move",
    "add_to_str",
    "add_folder_name",
    "numbering",
    "ext_replace",
]


class LastRename:
    """
    A last rename object that saves the previous renames and
    gives the ability to undo the changes

    A list of tuples where tuple[0] is the old name and
    tuple[1] the new name
    """

    def __init__(self):
        self.last_rename_list = []

    def appendRenamePair(self, past_name, new_name):
        """Appending new items"""
        pair_tuple = (past_name, new_name)
        self.last_rename_list.append(pair_tuple)

        return pair_tuple

    def lastRenameListGet(self):
        """Return the last rename array"""
        return self.last_rename_list

    def lastNameListGet(self):
        """Return the old name in the last rename"""
        last_name_list = list(
            last_name[0] for last_name in self.last_rename_list
        )
        return last_name_list

    def newNameListGet(self):
        """Return the selected new name in the last rename"""
        new_name_list = list(new_name[1] for new_name in self.last_rename_list)
        return new_name_list

    def clear(self):
        """Clear the last rename array"""
        self.last_rename_list = []

    def __str__(self):
        """Define how to print the oobject"""
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
            self, text="Command", command=apply_command
        )
        self.load_command_button.grid(
            column=0, row=1, padx=1, pady=1, sticky="e"
        )
        # Disable the button if no path to where commands are stored
        if not bpn.CONFIG_FOLDER_PATH:
            self.load_command_button.config(state="disable")

        self.reset_button = ttk.Button(self, text="Reset", command=full_reset)
        self.reset_button.grid(column=1, row=0, padx=1, pady=1, sticky="e")

        self.revert_button = ttk.Button(self, text="Undo", command=undo_rename)
        self.revert_button.grid(column=1, row=1, padx=1, pady=1, sticky="e")

        self.rename_button = ttk.Button(
            self, text="Rename", command=final_rename
        )
        self.rename_button.grid(
            column=2, row=0, rowspan=2, padx=1, pady=1, sticky="nse"
        )


def apply_command(event=None, command_name=None, *args, **kwargs):
    """
    Directly applies a command or a chain of commands.
    """
    # Clear the last_rename list
    bpn.last_rename.clear()
    # Save what the variable fields are right now
    var_val_dict_in_use = all_fields_get()

    # Gets the selected command if a command_name wasn't provided
    if not command_name:
        command_name = bpn.menu_bar.selectedCommandGet()

    # Apply only if the selected command isn't the default (no changes)
    if command_name != "DEFAULT":
        # Show that it's in the process
        info_bar.show_working()

        # Get the variables values dict from the config command file under
        # the selected command name
        var_val_dict = dict(bpn.COMMAND_CONF.items(command_name))

        # Set that variable values dict in the fields
        commands.set_command_call(var_val_dict)
        # Call for a basic Rename
        final_rename()

        # Get the next_step value from the command config, if there is one
        # call Apply_Command (this same function) but with command_name =
        # next_step
        next_step = var_val_dict["next_step"]
        if next_step:
            # Select the items that were previously selected based on the
            # last_rename list to get what are the new names
            bpn.fn_treeview.selectionSet(bpn.last_rename.newNameListGet())
            # Call Apply_Command with next_step
            apply_command(event=None, command_name=next_step)

        # Show that it finished
        inf_msg = 'Applied "{}" Command'.format(command_name)
        info_bar.finish_show_working(inf_msg=inf_msg)

    # If the selected command was the default show msg
    else:
        bpn.info_bar.lastActionRefresh("No Command Selected")

    # Set the variable fields back to what you had prior to the command
    commands.set_command_call(var_val_dict_in_use)


def undo_rename(*args, **kwargs):
    """
    Undo the last name changes.
    You can only undo 1 step back.
    """
    # Get a copy of the last changes list so when it gets modified it
    # doesnt affect this one and gets stuck in an infinite loop changing
    # back and forth
    # Undo the changes starting with the last one and going up
    last_rename_list = reversed(bpn.last_rename.lastRenameListGet())

    # Try to undo the changes only if there are changes to undo
    if last_rename_list:
        # Show that it's in the process
        info_bar.show_working()

        print("Undo:")
        for name_pair in last_rename_list:
            # Get the new path and the old path from the last
            # changes paths pairs
            new_path = name_pair[1]
            last_path = name_pair[0]

            # Apply a system rename
            system_rename(new_path, last_path)
        print()

        # Update the folders treeviews
        trees.refresh_treeviews()

        info_bar.finish_show_working(inf_msg="Finished Undo Operation")

        # Clear the last rename list pairs
        bpn.last_rename.clear()

    # Else show msg
    else:
        bpn.info_bar.lastActionRefresh("No Changes to Undo")


def final_rename(*args, **kwargs):
    """Change the selected items names according to the entry fields"""
    # Clear the last_rename action list
    bpn.last_rename.clear()
    # Get selected items
    sel_paths = list(bpn.fn_treeview.selectedItems())

    # When to reverse the naming items list so as to skip naming problems
    # like with recursiveness naming a folder before the files in it so
    # then the files can't be renamed because the path pointer doesn't
    # exists. Optimized the boolean function
    # A=menu_bar.renameBotTopGet()
    # B=nb.filters.depthGet()
    # C=nb.filters.reverseGet()
    # F(A,B,C)=~BA+B~C
    if (
        not bpn.filters_widget.fields.depth.get()
        and bpn.menu_bar.renameBotTopGet()
    ) or (
        bpn.filters_widget.fields.depth.get()
        and not bpn.filters_widget.fields.reverse.get()
    ):
        sel_paths = reversed(sel_paths)

    # Try to apply the changes only if there is a selection
    if sel_paths:
        # Show that its in the process
        info_bar.show_working()

        print("Rename:")
        for path in sel_paths:
            directory, slash, old_name = path.rpartition("/")
            name = bpn.fn_treeview.tree_folder.set(path, "#1")
            # Only rename if the old name is different from the new name
            if name != old_name:
                new_path = directory + slash + name

                system_rename(path, new_path)
            else:
                print('"{}" New name is the same as old name'.format(path))
        print()

        trees.refresh_treeviews()

        # Show that its finish
        info_bar.finish_show_working(inf_msg="Finished Rename")

    # Else show a msg that there is no selection
    else:
        bpn.info_bar.lastActionRefresh("No Selected Items")


def system_rename(file, new_path, *args, **kwargs):
    """Changes the name of the files in the system"""
    if not os.path.exists(new_path):
        try:
            os.rename(file, new_path)
            bpn.last_rename.appendRenamePair(file, new_path)

            print("{} -> {}".format(file, new_path))

        # Catch exceptions for invalid filenames
        except OSError:
            msg = f"Couldn't rename file {file}.\nInvalid characters"
            basewidgets.ErrorFrame(error_desc=msg)
            bpn.info_bar.lastActionRefresh(
                "Couldn't Rename file. Invalid characters"
            )

        except FileNotFoundError:
            msg = f"Couldn't rename file {file}.\nFile not found"
            basewidgets.ErrorFrame(error_desc=msg)
            bpn.info_bar.lastActionRefresh(
                "Couldn't Rename file. File not found"
            )

    # If path already exists don't write over it and skip it
    else:
        msg = (
            f'Couldn\'t rename file "{file}" to "{new_path}".\nPath already ex'
            "ists"
        )
        basewidgets.ErrorFrame(error_desc=msg)
        bpn.info_bar.lastActionRefresh(
            "Couldn't Rename file. Path already exists"
        )


def full_reset(*args, **kwargs):
    """Calls all resetWidget Methods"""
    bpn.rename_from_file.resetWidget()
    bpn.rename_from_reg_exp.resetWidget()
    bpn.name_basic.resetWidget()
    bpn.replace.resetWidget()
    bpn.case.resetWidget()
    bpn.remove.resetWidget()
    bpn.move_parts.resetWidget()
    bpn.add_to_str.resetWidget()
    bpn.add_folder_name.resetWidget()
    bpn.numbering.resetWidget()
    bpn.ext_replace.resetWidget()

    bpn.info_bar.lastActionRefresh("Full Reset")


def all_fields_get():
    return {
        **bpn.rename_from_file.fields.get_all(),
        **bpn.rename_from_reg_exp.fields.get_all(),
        **bpn.name_basic.fields.get_all(),
        **bpn.replace.fields.get_all(),
        **bpn.case.fields.get_all(),
        **bpn.remove.fields.get_all(),
        **bpn.move_parts.fields.get_all(),
        **bpn.add_to_str.fields.get_all(),
        **bpn.add_folder_name.fields.get_all(),
        **bpn.numbering.fields.get_all(),
        **bpn.ext_replace.fields.get_all(),
    }


def new_naming_visual(name, idx, path):
    return new_naming(name, idx, path, **all_fields_get())
