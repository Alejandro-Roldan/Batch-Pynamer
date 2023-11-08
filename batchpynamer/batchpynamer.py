#!/usr/bin/env python3

import os
import sys

import batchpynamer.config as bpn_config
import batchpynamer.gui as bpn_gui
from batchpynamer.config import config

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


def _start_path_handling(sys_args):
    """Get the path from the arguments in the program call or use a default
    path if no argument was passed"""

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
            f"path), got {len(sys_args) - 1} instead."
        )
    # When finding a FileNotFoundError exit the program with an error message
    except FileNotFoundError:
        sys.exit(f'ERROR:\n\t- The given path "{path}" doesn\'t exists.')
    # When finding a NotADirectoryError exit the program with an error message
    except NotADirectoryError:
        sys.exit(f'ERROR:\n\t- The given path "{path}" isn\'t a directory.')
    # When finding a PermissionError exit the program with an error message
    except PermissionError:
        sys.exit(
            "ERROR:\n\t- You don't have permission to access the given path"
            f' "{path}".'
        )
    # When there was no path given from the terminal default to the user path
    except IndexError:
        path = "."

    return path


def _gui_run():
    """
    PROGRAM INITIALIZATION
    """
    og_path = _start_path_handling(sys.argv)

    # Try to create the configuration folder
    if bpn_config.config_folder_path:
        config.create_config_folder(bpn_config.config_folder_path)
        config.create_config_folder(bpn_config.plugins_folder_path)

    """
    WINDOW INITIALIZATION
    """
    # Create the Tkinter root window
    bpn_gui.init_tk_root()
    # Initialize
    bpn_gui.root.tk_init(og_path)


###################################
"""
PROGRAM
"""
###################################
if __name__ == "__main__":
    _gui_run()
