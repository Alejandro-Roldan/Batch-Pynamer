from .. import basewidgets
import tkinter as tk
from tkinter import ttk

# Cant import files with numbers directly so use
# Equivalent to "import ... as ..."
# name_basic = __import__("", ["02_name_basic"])
from . import a_from_file
from . import b_reg_exp
from . import c_name_basic
from . import d_replace
from . import e_case
from . import f_remove
from . import g_move
from . import h_add_to_str
from . import i_add_folder_name
from . import j_numbering
from . import k_ext_replace
import batchpynamer

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


class Rename(basewidgets.BaseWidget, ttk.LabelFrame):
    """
    Draws the Rename button. Inside rename notebook. This is always last.
    It has:
        - Button that calls to permanently rename the selected files
        - Button that resets all fields inside the rename notebook
        - Button that reverts the last renaming action
    """

    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        # self.frame.grid(column=1, row=0, columnspan=5, sticky='w'+'e')
        self.frame.grid(column=1, row=0, sticky="w" + "e")
        # self.frame.columnconfigure(0, weight=1)

        self.load_command_button = ttk.Button(
            self.frame, text="Command", command=self.Apply_Command
        )
        self.load_command_button.grid(
            column=0, row=1, padx=1, pady=1, sticky="e"
        )
        # Disable the button if no path to where commands are stored
        if not CONFIG_FOLDER_PATH:
            self.load_command_button.config(state="disable")

        self.reset_button = ttk.Button(
            self.frame, text="Reset", command=self.Full_Reset
        )
        self.reset_button.grid(column=1, row=0, padx=1, pady=1, sticky="e")

        self.revert_button = ttk.Button(
            self.frame, text="Undo", command=self.Undo
        )
        self.revert_button.grid(column=1, row=1, padx=1, pady=1, sticky="e")

        self.rename_button = ttk.Button(
            self.frame, text="Rename", command=self.Final_Rename
        )
        self.rename_button.grid(
            column=2, row=0, rowspan=2, padx=1, pady=1, sticky="nse"
        )

    @staticmethod
    def Full_Reset(*args, **kwargs):
        """Calls all resetWidget Methods"""
        nb.rename_from_file.resetWidget()
        nb.reg_exp.resetWidget()
        nb.name_basic.resetWidget()
        nb.replace.resetWidget()
        nb.case.resetWidget()
        nb.remove.resetWidget()
        nb.Move_Parts.resetWidget()
        nb.add_to_string.resetWidget()
        nb.append_folder_name.resetWidget()
        nb.numbering.resetWidget()
        nb.extension_rep.resetWidget()

        inf_bar.lastActionRefresh("Full Reset")

    @staticmethod
    def Apply_Command(event=None, command_name=None, *args, **kwargs):
        """
        Directly applies a command or a chain of commands.
        """
        # Clear the last_rename list
        last_rename.clear()
        # Save what the variable fields are right now
        var_val_dict_in_use = Create_Var_Val_Dict()

        # Gets the selected command if a command_name wasn't provided
        if not command_name:
            command_name = menu_bar.selectedCommandGet()

        # Apply only if the selected command isn't the default (no changes)
        if command_name != "DEFAULT":
            # Show that it's in the process
            Show_Working()

            # Get the variables values dict from the config command file under
            # the selected command name
            var_val_dict = dict(COMMAND_CONF.items(command_name))

            # Set that variable values dict in the fields
            Set_Command_Call(var_val_dict)
            # Call for a basic Rename
            Rename.Final_Rename()

            # Get the next_step value from the command config, if there is one
            # call Apply_Command (this same function) but with command_name =
            # next_step
            next_step = var_val_dict["next_step"]
            if next_step:
                # Select the items that were previously selected based on the
                # last_rename list to get what are the new names
                fn_treeview.selectionSet(last_rename.newNameListGet())
                # Call Apply_Command with next_step
                Rename.Apply_Command(event=None, command_name=next_step)

            # Show that it finished
            inf_msg = 'Applied "{}" Command'.format(command_name)
            Finish_Show_Working(inf_msg=inf_msg)

        # If the selected command was the default show msg
        else:
            inf_bar.lastActionRefresh("No Command Selected")

        # Set the variable fields back to what you had prior to the command
        Set_Command_Call(var_val_dict_in_use)

    @staticmethod
    def Undo(*args, **kwargs):
        """
        Undo the last name changes.
        You can only undo 1 step back.
        """
        # Get a copy of the last changes list so when it gets modified it
        # doesnt affect this one and gets stuck in an infinite loop changing
        # back and forth
        # Undo the changes starting with the last one and going up
        last_rename_list = reversed(last_rename.lastRenameListGet())

        # Try to undo the changes only if there are changes to undo
        if last_rename_list:
            # Show that it's in the process
            Show_Working()

            print("Undo:")
            for name_pair in last_rename_list:
                # Get the new path and the old path from the last
                # changes paths pairs
                new_path = name_pair[1]
                last_path = name_pair[0]

                # Apply a system rename
                System_Rename(new_path, last_path)
            print()

            # Update the folders treeviews
            Refresh_Treeviews()

            Finish_Show_Working(inf_msg="Finished Undo Operation")

            # Clear the last rename list pairs
            last_rename.clear()

        # Else show msg
        else:
            inf_bar.lastActionRefresh("No Changes to Undo")

    @staticmethod
    def Final_Rename(*args, **kwargs):
        """Change the selected items names according to the entry fields"""
        # Clear the last_rename action list
        last_rename.clear()
        # Get selected items
        sel_paths = list(fn_treeview.selectedItems())

        # When to reverse the naming items list so as to skip naming problems
        # like with recursiveness naming a folder before the files in it so
        # then the files can't be renamed because the path pointer doesn't
        # exists. Optimized the boolean function
        # A=menu_bar.renameBotTopGet()
        # B=nb.filters.depthGet()
        # C=nb.filters.reverseGet()
        # F(A,B,C)=~BA+B~C
        if (not nb.filters.depthGet() and menu_bar.renameBotTopGet()) or (
            nb.filters.depthGet() and not nb.filters.reverseGet()
        ):
            sel_paths = reversed(sel_paths)

        # Try to apply the changes only if there is a selection
        if sel_paths:
            # Show that its in the process
            Show_Working()

            print("Rename:")
            for path in sel_paths:
                directory, slash, old_name = path.rpartition("/")
                name = fn_treeview.tree_folder.set(path, "#1")
                # Only rename if the old name is different from the new name
                if name != old_name:
                    new_path = directory + slash + name

                    System_Rename(path, new_path)
                else:
                    print('"{}" New name is the same as old name'.format(path))
            print()

            Refresh_Treeviews()

            # Show that its finish
            Finish_Show_Working(inf_msg="Finished Rename")

        # Else show a msg that there is no selection
        else:
            inf_bar.lastActionRefresh("No Selected Items")


def new_naming_x(name, idx, path):
    return new_naming(
        name,
        idx,
        path,
        **batchpynamer.rename_from_file.fields.get_all(),
        **batchpynamer.rename_from_reg_exp.fields.get_all(),
        **batchpynamer.name_basic.fields.get_all(),
        **batchpynamer.replace.fields.get_all(),
        **batchpynamer.case.fields.get_all(),
        **batchpynamer.remove.fields.get_all(),
        **batchpynamer.move_parts.fields.get_all(),
        **batchpynamer.add_to_str.fields.get_all(),
        **batchpynamer.add_folder_name.fields.get_all(),
        **batchpynamer.numbering.fields.get_all(),
        **batchpynamer.ext_replace.fields.get_all(),
    )


def new_naming(name, idx, path, **fields_dict):
    """
    Creates the new name going through all fields and making the changes
    to the old_name string
    """
    # Separate name and extension
    name, ext = De_Ext(name)

    # name = Rename_From_File.Rename_From_File_Rename(name, idx)  # (0)
    name = a_from_file.rename_from_file_rename(name, idx, **fields_dict)  # (0)
    # name = Reg_Exp.Reg_Exp_Rename(name)                         # (1)
    name = b_reg_exp.reg_exp_rename(name, **fields_dict)  # (1)
    name = c_name_basic.name_basic_rename(name, **fields_dict)  # (2)
    # name = Replace.Replace_Action(name)                         # (3)
    name = d_replace.replace_action(name, **fields_dict)  # (3)
    # name = Case.Case_Change(name)                               # (4)
    name = e_case.case_change(name, **fields_dict)  # (4)
    # name = Remove.Remove_Rename(name)                           # (5)
    name = f_remove.remove_rename(name, **fields_dict)  # (5)
    # name = Move_Parts.Move_Copy_Action(name)                    # (6)
    name = g_move.move_copy_action(name, **fields_dict)  # (6)
    # name = Add_To_String.Add_Rename(name)                       # (7)
    name = h_add_to_str.add_rename(name, **fields_dict)  # (7)
    # name = Append_Folder_Name.Append_Folder_Rename(name, path)  # (8)
    name = i_add_folder_name.add_folder_rename(
        name, path, **fields_dict
    )  # (8)
    # name = Numbering.Numbering_Rename(name, idx)                # (9)
    name = j_numbering.numbering_rename(name, idx, **fields_dict)  # (9)

    # ext = Extension_Rep.Extension_Rename(ext)                   # (10)
    ext = k_ext_replace.ext_rename(ext, **fields_dict)  # (10)

    # Remove leading and trailing whitespaces and re-add the extension
    name = name.strip() + ext

    # Format any metadata fields that have been added to the name
    # (only if the metadata modules were imported)
    # if batchpynamer.METADATA_IMPORT:
    #     name = Meta_Format(name, path)

    return name


def De_Ext(name):
    """
    Removes the extension from the selected path.
    Returns the name of the field and the extension separate.
    If theres no extension returns an empty extension.
    """
    file_name, dot, ext = name.rpartition(".")
    if file_name != "":
        ext = dot + ext
        name = file_name
    else:
        ext = ""

    return name, ext
