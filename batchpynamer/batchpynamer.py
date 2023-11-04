#!/usr/bin/env python3

""" Copyright 2019-2023 Alejandro Roldán """

"""
    This file is part of Batch Pynamer.

    Batch Pynamer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Batch Pynamer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Batch Pynamer.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import pathlib
import sys

import batchpynamer as bpn
from batchpynamer import mainwindow


def start_Path_Handling(sys_args):
    """Get the path from the arguments in the program call or use a default path
    if no argument was passed"""

    try:
        # Make sure the path doesn't have a trailing backslash to avoid errors
        # Except if its the root directory
        if sys_args[1] != "/":
            path = sys_args[1].rstrip("/")
        else:
            path = "/"

        # When more than 1 argument is provided raise an AttributeError
        if len(sys_args) > 2:
            raise AttributeError
        # When the given path doesnt exists raise a FileNotFoundError
        elif not os.path.exists(path):
            raise FileNotFoundError
        # When it exists but its not a directory raise a NotADirectoryError
        elif not os.path.isdir(path):
            raise NotADirectoryError
        # When you dont have permission to read or write that directory raise
        # a PermissionError
        elif not (os.access(path, os.R_OK) or os.access(path, os.W_OK)):
            raise PermissionError

    # When finding an AttributeError exit the program with an error message
    except AttributeError:
        sys.exit(
            "ERROR:\n\t- Too many arguments. Program expected 1 (a valid "
            "path), got {} instead.".format(len(sys_args) - 1)
        )
    # When finding a FileNotFoundError exit the program with an error message
    except FileNotFoundError:
        sys.exit(
            'ERROR:\n\t- The given path "{}" doesn\'t exists.'.format(path)
        )
    # When finding a NotADirectoryError exit the program with an error message
    except NotADirectoryError:
        sys.exit(
            'ERROR:\n\t- The given path "{}" isn\'t a directory.'.format(path)
        )
    # When finding a PermissionError exit the program with an error message
    except PermissionError:
        sys.exit(
            "ERROR:\n\t- You don't have permission to access the given path"
            ' "{}".'.format(path)
        )
    # When there was no path given from the terminal default to the user path
    except IndexError:
        path = "/home/Jupiter/Music"
        pass

    return path


def get_Max_Name_Len(path):
    """Get the maximum filename lenght in the active drive"""
    max_name_len = os.statvfs(path).f_namemax


def create_Config_Folder(path):
    """Creates the config folder if it doesn't exist already"""
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass


def _run():
    """
    PROGRAM INITIALIZATION
    """
    bpn.OG_PATH = start_Path_Handling(sys.argv)

    # Try to create the configuration folder
    if bpn.CONFIG_FOLDER_PATH:
        create_Config_Folder(bpn.CONFIG_FOLDER_PATH)

    """
    WINDOW INITIALIZATION
    """
    # Create the Tkinter root window
    bpn.init_tk_root()
    # Initialize
    bpn.root.tk_init()


###################################
"""
PROGRAM
"""
###################################
if __name__ == "__main__":
    _run()

    print("end")
