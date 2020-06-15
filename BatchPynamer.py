#!/usr/bin/env python3

import sys
import os
import pathlib
import configparser

import webbrowser   # for the About menu

import string
import unicodedata
import re               # regular expressions

import tkinter as tk
from tkinter import ttk

# All previous imports are basic python libraries

# Import for the metadata, optional
try:
    # Metadata imports
    from mutagen.flac import FLAC
    # Change import name for code clarity
    from mutagen.flac import Picture as FlacPicture

    from mutagen.easyid3 import EasyID3, EasyID3KeyError
    from mutagen.id3 import ID3, APIC
    from mutagen.mp3 import MP3

    from mutagen.easymp4 import EasyMP4, EasyMP4KeyError

    # Image manipulation imports
    from io import BytesIO
    import PIL
    import PIL.ImageTk

    # Set a flag
    METADATA_IMPORT = True

except ImportError:
    METADATA_IMPORT = False


###############################################################################
'''
    INDEX:
        - Vertical Scrollable Frame
        - Error Frame
        - Last Rename

        - Menubar
        - Tree System Navigation
        - File Folder Navigation
        - Directory entry for File Folder Navigation
        - Notebook
        - Extra Information Bar

        - Rename from file frame
        - Regular Expressions frame
        - Name frame
        - Replace frame
        - Case frame
        - Remove frame
        - Remove/Copy frame
        - Add to string frame
        - Append folder name frame
        - Numbering Frame
        - Extension replacement frame
        - Rename buttons frame

        - Metadata listentries frame
        - Metadata image frame
        - Metadata changes applier frame

        - Config, logs & commands classes and functions

        - General functions

        - Main function
'''
###############################################################################


###################################
'''
GLOBAL CONSTANTS
'''
###################################


APP_NAME = 'Batch Pynamer'
APP_VER = 6.00
TITLE = '{}-V{}'.format(APP_NAME, APP_VER)

PROJECT_URL = 'https://github.com/Alejandro-Roldan/Batch-Pynamer'


# Get the path from the arguments in the program call or use a default path
# if no argument was passed
try:
    PATH = sys.argv[1]
    # When more than 1 argument is provided raise an AttributeError
    if len(sys.argv) > 2:
        raise AttributeError
    # When the given path doesnt exists raise a FileNotFoundError
    elif not os.path.exists(PATH):
        raise FileNotFoundError
    # When it exists but its not a directory raise a NotADirectoryError
    elif not os.path.isdir(PATH):
        raise NotADirectoryError
    # When you dont have permission to read or write that directory raise
    # a PermissionError
    elif not (os.access(PATH, os.R_OK) or os.access(PATH, os.W_OK)):
        raise PermissionError
# When finding an AttributeError exit the program with an error message
except AttributeError:
    sys.exit('ERROR:\n\t- Too many arguments. Program expected 1 (a valid '\
                'path), got {} instead.'.format(len(sys.argv) - 1))
# When finding a FileNotFoundError exit the program with an error message
except FileNotFoundError:
    sys.exit('ERROR:\n\t- The given path "{}" doesn\'t exists.'.format(PATH))
# When finding a NotADirectoryError exit the program with an error message
except NotADirectoryError:
    sys.exit('ERROR:\n\t- The given path "{}" isn\'t a directory.'.format(PATH))
# When finding a PermissionError exit the program with an error message
except PermissionError:
    sys.exit('ERROR:\n\t- You don\'t have permission to access the given path'\
                ' "{}".'.format(PATH))
# When there was no path given from the terminal default to the user path
except IndexError:
    PATH = os.path.expanduser('~')

# Get the maximum filename lenght * 2 in the active drive
MAX_NAME_LEN = (os.statvfs(PATH).f_namemax)*2

# Configuration folder path depending on OS
if sys.platform == 'linux':
    CONFIG_FOLDER_PATH = os.path.expanduser('~/.config/batchpynamer/')
elif sys.platform == 'win32':
    CONFIG_FOLDER_PATH = os.path.expanduser('~/AppData/Roaming/batchpynamer/')
elif sys.platform == 'darwin':  # macOS
    CONFIG_FOLDER_PATH = os.path.expanduser('~/Library/Preferences/batchpynamer/')
else:
    CONFIG_FOLDER_PATH = None

# Configparser object for loading the commands
if CONFIG_FOLDER_PATH is not None:
    COMMAND_CONF_FILE = CONFIG_FOLDER_PATH + 'commands.conf'
    COMMAND_CONF = configparser.ConfigParser()
    COMMAND_CONF.read(COMMAND_CONF_FILE)


###################################
'''
WIDGET CREATION CLASSES
'''
###################################


class VerticalScrolledFrame(ttk.Frame):
    '''
        A pure Tkinter scrollable frame that actually works!
        * Use the 'interior' attribute to place widgets inside the scrollable frame
        * Construct and pack/place/grid normally
        * This frame only allows vertical scrolling
    '''
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand='false')
        canvas = tk.Canvas(
                            self, bd=0,
                            background='gray85',
                            highlightthickness=0,
                            yscrollcommand=vscrollbar.set,
                            )
        canvas.pack(side='left', fill='both', expand='true')
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class Error_Frame:
    def __init__(self, error_desc='', *args, **kwargs):
        self.error_frame = tk.Toplevel(root, bg='gray85')
        self.error_frame.title('Error Window')
        self.error_frame.attributes('-type', 'dialog')

        ttk.Label(
                    self.error_frame,
                    text='Error: {}'.format(error_desc)
                    ).grid(column=0, row=0, padx=5, pady=5)

        ttk.Button(
                    self.error_frame,
                    text="Okay",
                    command=self.error_frame.destroy
                    ).grid(column=0, row=1, padx=5, pady=5)


class Last_Rename:
    def __init__(self, *args, **kwargs):
        self.last_rename_list = []

    def appendRenamePair(self, past_name, new_name, *args, **kwargs):
        pair_tuple = (past_name, new_name)
        self.last_rename_list.append(pair_tuple)

        return pair_tuple

    def lastRenameListGet(self, *args, **kwargs):
        return self.last_rename_list

    def lastNameListGet(self, *args, **kwargs):
        last_name_list = list(last_name[0] for last_name in self.last_rename_list)
        return last_name_list

    def newNameListGet(self, *args, **kwargs):
        new_name_list = list(new_name[1] for new_name in self.last_rename_list)
        return new_name_list

    def clear(self, *args, **kwargs):
        self.last_rename_list = []

    def __str__(self, *args, **kwargs):
        return str(self.last_rename_list)


###################################
'''
BASIC WIDGET CLASSES
'''
###################################


class Top_Menu:
    def __init__(self, master, *args, **kwargs):
        self.menubar = tk.Menu(master, bg='gray75', foreground='black')

        # Create the menus and add them to the main bar
        self.fileMenu()
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.selectionMenu()
        self.menubar.add_cascade(label="Selection", menu=self.selection_menu)

        # Only create the command menu if there is a configuration folder
        self.commandMenu()
        self.menubar.add_cascade(label="Commands", menu=self.command_menu)
        if not CONFIG_FOLDER_PATH:
            self.menubar.entryconfigure(index=3, state='disable')

        self.menubar.add_command(label='About', command=self.openProjectUrl)

        self.metadataDisable()

    def fileMenu(self, *args, **kwargs):
        ''' File Menu Dropdown '''
        self.rename_bot_top = tk.BooleanVar()

        # Create the menu
        self.file_menu = tk.Menu(
                                    self.menubar,
                                    tearoff=0,
                                    bg='gray75',
                                    foreground='black'
                                    )

        # Rename
        self.file_menu.add_command(
                                    label='Rename',
                                    command=Rename.Final_Rename,
                                    accelerator='Ctrl+R'
                                    )

        # Undo Rename
        self.file_menu.add_command(
                                    label='Undo Rename',
                                    command=Rename.Undo,
                                    accelerator='Ctrl+Z'
                                    )

        # Reset Entry Fields
        self.file_menu.add_command(
                                    label='Reset Entry Fields',
                                    command=Rename.Full_Reset,
                                    accelerator='Ctrl+T'
                                    )

        # Rename from Bottom to Top
        self.file_menu.add_checkbutton(
                                    label='Activate renaming from Bottom to Top',
                                    variable=self.rename_bot_top
                                    )

        # Separator
        self.file_menu.add_separator()

        # Create the metadata menu options only if the metadata modification
        # is active (the dependencies have been exported)
        if METADATA_IMPORT:
            # Apply Metadata Changes
            self.file_menu.add_command(
                                        label='Apply Metadata Changes',
                                        command=nb.apply_changes.metaChangesCall,
                                        )

            # Apply Image Metadata
            self.file_menu.add_command(
                                        label='Apply Image Metadata Change',
                                        command=nb.apply_changes.imgChangesCall
                                        )

            # Apply Both Image & Metadata Changes
            self.file_menu.add_command(
                                        label='Apply Both Image & Metadata Changes',
                                        command=nb.apply_changes.allChangesCall
                                        )

            # Set the title and the tracknumber metadata from the filename
            self.file_menu.add_command(
                                        label='Set "title" & "tracknumber" from filename',
                                        command=Title_Track_From_File
                                        )

            # Format tracknumber metadata field
            self.file_menu.add_command(
                                        label='Format "tracknumber"',
                                        command=Format_Track_Num_Meta
                                        )

            # Separator
            self.file_menu.add_separator()

        # Refresh Files
        self.file_menu.add_command(
                                    label='Refresh Files',
                                    command=fn_treeview.refreshView,
                                    accelerator='F5'
                                    )

        # Refresh Tree
        self.file_menu.add_command(
                                    label='Refresh Tree',
                                    command=dir_entry_frame.folderNavRefresh,
                                    accelerator='Ctrl+F5'
                                    )

        # Separator
        self.file_menu.add_separator()

        # Exit
        self.file_menu.add_command(
                                    label='Exit',
                                    command=root.quit
                                    )

    def renameBotTopGet(self, *args, **kwargs):
        return self.rename_bot_top.get()

    def selectionMenu(self, *args, **kwargs):
        ''' Selection Menu Dropdown '''
        # Create the menu
        self.selection_menu = tk.Menu(
                                        self.menubar,
                                        tearoff=0,
                                        bg='gray75',
                                        foreground='black'
                                        )

        # Select All
        self.selection_menu.add_command(
                                        label='Select All',
                                        command=fn_treeview.selectAll,
                                        accelerator='Ctrl+A'
                                        )

        # Deselect All
        self.selection_menu.add_command(
                                        label='Deselect All',
                                        command=fn_treeview.deselectAll,
                                        accelerator='Ctrl+D'
                                        )

        # Invert Selection
        self.selection_menu.add_command(
                                        label='Invert Selection',
                                        command=fn_treeview.invertSelection,
                                        accelerator='Ctrl+I'
                                        )

    def commandMenu(self, *args, **kwargs):
        ''' Command Menu Dropdown '''
        # Variable defs
        self.selected_command = tk.StringVar(value='DEFAULT')

        # Create the menu
        self.command_menu = tk.Menu(
                                    self.menubar,
                                    tearoff=0,
                                    bg='gray75',
                                    foreground='black'
                                    )

        # Save current variable values entries as command
        self.command_menu.add_command(
                                        label='Save Field States to Command',
                                        command=Save_Command_Name_Window
                                        )

        # Load selected command
        self.command_menu.add_command(
                                        label='Load Field States from Command',
                                        command=Load_Command_Call,
                                        accelerator='Ctrl+E'
                                        )

        # Apply selected command
        self.command_menu.add_command(
                                        label='Apply Selected Command',
                                        command=Rename.Apply_Command
                                        )

        # Delete selected command
        self.command_menu.add_command(
                                        label='Delete Selected Command',
                                        command=Delete_Command
                                        )

        self.command_select_menu = tk.Menu(
                                            self.command_menu,
                                            tearoff=0,
                                            bg='gray75',
                                            foreground='black'
                                            )

        # Only try to load the commands if there is a path to the
        # commands configuration file
        if CONFIG_FOLDER_PATH:
            self.updateCommandListMenu()

        # Separator
        self.command_menu.add_separator()

        # Apply selected command
        self.command_menu.add_cascade(
                                        label='Select Command',
                                        menu=self.command_select_menu
                                        )

    def updateCommandListMenu(self, *args, **kwargs):
        ''' Deletes the already existing items and updates the view '''
        self.command_select_menu.delete(0, 'end')
        # Read the commands config and create a radio button for each command
        for command_name in COMMAND_CONF.sections():
            self.command_select_menu.add_radiobutton(
                                                label=command_name,
                                                variable=self.selected_command,
                                                value=command_name
                                                )

    def renameEnable(self, *args, **kwargs):
        self.file_menu.entryconfigure(index=0, state='active')
        self.file_menu.entryconfigure(index=1, state='active')
        self.file_menu.entryconfigure(index=2, state='active')

    def renameDisable(self, *args, **kwargs):
        self.file_menu.entryconfigure(index=0, state='disable')
        self.file_menu.entryconfigure(index=1, state='disable')
        self.file_menu.entryconfigure(index=2, state='disable')

    def metadataEnable(self, *args, **kwargs):
        if METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state='active')
            self.file_menu.entryconfigure(index=6, state='active')
            self.file_menu.entryconfigure(index=7, state='active')
            self.file_menu.entryconfigure(index=8, state='active')
            self.file_menu.entryconfigure(index=9, state='active')

    def metadataDisable(self, *args, **kwargs):
        if METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state='disable')
            self.file_menu.entryconfigure(index=6, state='disable')
            self.file_menu.entryconfigure(index=7, state='disable')
            self.file_menu.entryconfigure(index=8, state='disable')
            self.file_menu.entryconfigure(index=9, state='disable')

    def selectedCommandGet(self, *args, **kwargs):
        return self.selected_command.get()

    def openProjectUrl(self, *args, **kwargs):
        ''' Open the Project Url when clicking the about menu option '''
        webbrowser.open(PROJECT_URL)


class TreeNavigator:
    def __init__(self, master, path, *args, **kwargs):
        '''
        Draws the treeview of the file navigation:
            It exclusively shows folders.
            You can only select one item at a time.
            It creates a temporary child node (empty) inside the folders to be
            able to open them without having to load the directories inside.
            If this wasn't done the app would have to load the whole system
            at starup.
        '''
        self.path = path

        # Create a dict of what nodes exist. Used to load the placeholder nodes
        self.nodes = {}

        frame = ttk.Frame(master)
        frame.grid(row=1, column=0)

        # Directory navigator, treeview
        self.tree_nav = ttk.Treeview(frame, selectmode='browse')
        # Scroll bars tree file navigation
        ysb_tree_nav = ttk.Scrollbar(
                                        frame,
                                        orient='vertical',
                                        command=self.tree_nav.yview
                                        )
        xsb_tree_nav = ttk.Scrollbar(
                                        frame,
                                        orient='horizontal',
                                        command=self.tree_nav.xview
                                        )
        self.tree_nav.configure(
                                yscroll=ysb_tree_nav.set,
                                xscroll=xsb_tree_nav.set
                                )
        # Title of the Treeview
        self.tree_nav.heading('#0', text='Browse Files', anchor='w')
        self.tree_nav.column('#0', width=280)
        # Treeview and the scrollbars placing
        self.tree_nav.grid(row=0, column=0)
        ysb_tree_nav.grid(row=0, column=1, sticky='ns')
        xsb_tree_nav.grid(row=1, column=0, sticky='ew')

        self.bindEntries()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # Tree navigation bindings
        self.tree_nav.bind('<<TreeviewOpen>>', self.openNode)
        self.tree_nav.bind('<<TreeviewSelect>>', fn_treeview.refreshView)

    def selectedItem(self, *args, **kwargs):
        # Since this tree can only select 1 item at a time we just pass
        # the index instead of doing a for loop
        return self.tree_nav.focus()

    def deleteChildren(self, path='', *args, **kwargs):
        ''' Delete already existing nodes in the folder view '''
        for child in self.tree_nav.get_children(path):
            self.tree_nav.delete(child)

    def insertNode(self, entry, *args, **kwargs):
        ''' Create nodes for the tree file navigation. '''
        parent = os.path.dirname(entry.path)

        # Uses the absolute path to the folder as the iid
        node = self.tree_nav.insert(
                                    parent=parent,
                                    index='end',
                                    iid=entry.path,
                                    text=entry.name,
                                    open=False
                                    )

        # Make dirs openable without loading children by creating an empty
        # node inside
        self.nodes[node] = entry.path
        self.tree_nav.insert(parent=node, index='end')

    def openNode(self, *args, **kwargs):
        ''' Open Node action. Only avaible to the tree file navigation. '''
        # Get active node
        path = self.tree_nav.focus()

        # Get the path to the directory of the opening node and only act when
        # it finds it in the dictionary (which means the node hasn't been
        # opened previously, if it where then there would be no need to reload
        # the contents)
        if self.nodes.pop(path, None):
            # Delete the placeholder node that was created previously
            self.tree_nav.delete(self.tree_nav.get_children(path))

            # Get if we need to show hidden folders
            hidden = nb.filters.hiddenGet()
            # Get folders and sort them
            scanned_dir = Scandir_Recursive(path=path, folders=True,
                                            files=False, hidden=hidden,
                                            depth=0)
            scanned_dir = Tree_Sort(tree=scanned_dir)
            # Insert the entries
            for entry in scanned_dir:
                self.insertNode(entry)

    def refreshView(self, *args, **kwargs):
        path = self.path
        # Get if hidden folders are active
        hidden = nb.filters.hiddenGet()

        # Delete all children and reset Treeview
        self.deleteChildren()
        # Insert the original node
        self.tree_nav.insert(
                                parent='',
                                index='end',
                                iid=self.path,
                                text=self.path,
                                open=True
                                )

        scanned_dir = Scandir_Recursive(path=path, folders=True,
                                        files=False, hidden=hidden, depth=0)
        scanned_dir = Tree_Sort(tree=scanned_dir)

        for entry in scanned_dir:
            self.insertNode(entry)

    def updateNode(self, *args, **kwargs):
        '''
            Updates the focused node.
            Close focused node, deletes all children and inserts an empty node
        '''
        path = self.tree_nav.focus()
        # Close focused node
        self.tree_nav.item(path, open=False)
        # Delete children nodes of the focused node
        self.deleteChildren(path)

        # Reinsert an empty node
        self.tree_nav.insert(path, 'end')
        self.nodes[path] = path


class FileNavigator:
    '''
    Draws the treeview of the files and folders inside the selected folder.
    '''
    def __init__(self, master, *args, **kwargs):
        frame = ttk.Frame(master)
        frame.grid(row=1, column=1, sticky='w'+'e')
        frame.columnconfigure(2, weight=1)

        self.active_path = ''

        # File selection, treeview
        self.tree_folder = ttk.Treeview(frame, selectmode='extended')

        # Scroll bars tree selected folder
        ysb_tree_folder = ttk.Scrollbar(
                                        frame,
                                        orient='vertical',
                                        command=self.tree_folder.yview
                                        )
        xsb_tree_folder = ttk.Scrollbar(
                                        frame,
                                        orient='horizontal',
                                        command=self.tree_folder.xview
                                        )
        self.tree_folder.configure(
                                    yscroll=ysb_tree_folder.set,
                                    xscroll=xsb_tree_folder.set
                                    )
        # Name first column
        self.tree_folder.heading('#0', text='Old Name', anchor='w')
        # Create second column and name it
        self.tree_folder['columns'] = ('#1')
        self.tree_folder.heading('#1', text='New name', anchor='w')
        # Treeview and the scrollbars placing
        self.tree_folder.grid(row=0, column=2, sticky='w'+'e')
        ysb_tree_folder.grid(row=0, column=3, sticky='ns')
        xsb_tree_folder.grid(row=1, column=2, sticky='ew')

        # Bindings
        self.bindEntries()

    def oldNameGet(self, item, *args, **kwargs):
        return fn_treeview.tree_folder.item(item)['text']

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # File Navigation bindings
        self.tree_folder.bind('<<TreeviewSelect>>', Populate_Fields)
        self.tree_folder.bind('<<TreeviewSelect>>', Call_For_Info_Bar, add='+')
        self.tree_folder.bind('<Button-3>', self.rightClickPathToClip)

    def selectionSet(self, items, *args, **kwargs):
        ''' Sets the selection of the tree_folder to the list of items '''
        self.tree_folder.selection_set(items)

    def selectAll(self, *args, **kwargs):
        ''' Select all children items'''
        self.tree_folder.selection_set(self.tree_folder.get_children())

    def deselectAll(self, *args, **kwargs):
        ''' Deselect all selected items '''
        self.tree_folder.selection_set()

    def invertSelection(self, *args, **kwargs):
        ''' Inverts the selection '''
        # Get all children
        all_items = self.tree_folder.get_children()

        # Get current selection
        selected = self.selectedItems()
        # Create a list of items from all_items that aren't in selected
        inverted = [item for item in all_items if item not in selected]

        # Set inverted as the new selection
        self.selectionSet(inverted)

    def deleteChildren(self, *args, **kwargs):
        ''' Delete already existing nodes in the folder view '''
        for item in self.tree_folder.get_children():
            self.tree_folder.delete(item)

    def setNewName(self, path, new_name, old_name, *args, **kwargs):
        return self.tree_folder.set(path, '#1', new_name)

    def selectedItems(self, *args, **kwargs):
        return self.tree_folder.selection()

    def showNewName(self, *args, **kwargs):
        '''
            Iterates over each selected item and recreates each new name
            following the renaming rules given inside the rename page of
            the notebook.
        '''
        # get list of selected items iids
        selection = self.selectedItems()
        for idx, path in enumerate(selection):
            # get the old name
            old_name = self.oldNameGet(path)
            # transform the old name to the new name
            new_name = New_Naming(old_name, idx, path)
            # changes the new name column
            self.setNewName(path, new_name, old_name)

    def resetNewName(self, *args, **kwargs):
        '''
            Renames every item to their old name, so if you change selection
            they dont still show the new name.
        '''
        all_nodes = self.tree_folder.get_children()
        for item in all_nodes:
            old_name = self.oldNameGet(item)
            self.setNewName(item, old_name, old_name)

    def rightClickPathToClip(self, event, *args, **kwargs):
        '''
            When you right click over an item in the folder treeview gets the
            path to that item and puts it in the clipboard so you can paste it
            somewhere elese.
        '''
        # Get the path of the item in the row under the cursor position
        path = self.tree_folder.identify_row(event.y)
        # Clear the clipboard
        root.clipboard_clear()
        # Copy path to clipboard
        root.clipboard_append(path)
        # Get the file/directory name to use in info msg
        name = os.path.basename(path)

        # Set info msg
        inf_bar.lastActionRefresh('Copied "{}" Path to Clipboard'.format(name))        

    def insertNode(self, entry, tag='', *args, **kwargs):
        ''' Create nodes '''
        # uses the absolute path to the folder as the iid
        self.tree_folder.insert(
                                parent='',
                                index='end',
                                iid=entry.path,
                                text=entry.name,
                                values=[entry.name],
                                tags=tag,
                                open=False
                                )

    def refreshView(self, event=None, path='', tree=[], *args, **kwargs):
        ''' Get the folder path and update the treeview '''
        # Get selected folder's path
        path = folder_treeview.selectedItem()
        # When the path isn't set use the active_path
        if not path:
            path = self.active_path

        # If after that the path is still empty (when a folder hasn't been
        # selected) don't try to load it
        if path:
            # Get the filters values
            mask = nb.filters.maskGet()
            ext = nb.filters.extGet()
            folders = nb.filters.foldersGet()
            files = nb.filters.filesGet()
            hidden = nb.filters.hiddenGet()
            files_before_dirs = nb.filters.filesBeforeDirsGet()
            reverse = nb.filters.reverseGet()
            min_len = nb.filters.nameLenMinGet()
            max_len = nb.filters.nameLenMaxGet()
            depth = nb.filters.depthGet()

            # Compile the regular expressions mask
            mask = re.compile(mask)

            # Transform the list of extensions into a tuple and add a . before the
            # extension to make sure that its an extension and not just that the
            # filename ends in that
            ext_list = ['.' + i for i in re.split('; |;|, |,', ext)]
            try:
                ext_list.remove('.')
            except ValueError:
                pass
            ext_tuple = tuple(ext_list)

            # Delete the children, load the new ones and sort them
            self.deleteChildren()

            scanned_dir = Scandir_Recursive(path, mask=mask,
                                            ext_tuple=ext_tuple,
                                            folders=folders, files=files,
                                            hidden=hidden, min_len=min_len,
                                            max_len=max_len, depth=depth)
            scanned_dir = Tree_Sort(tree=scanned_dir, depth=depth,
                                    files_before_dirs=files_before_dirs,
                                    reverse=reverse)

            for entry in scanned_dir:
                self.insertNode(entry)

            # Call info set actions
            self.active_path = path
            inf_bar.numItemsRefresh()
            dir_entry_frame.folderDirSet()
            inf_bar.lastActionRefresh('Refreshed File View')


class DirEntryFrame:
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=0, row=0, columnspan=2, sticky='w'+'e')
        # Set the weight of the entry column so it extends the whole frame
        self.frame.columnconfigure(1, weight=1)

        self.folder_dir = tk.StringVar()

        # Folder Navigation Refresh, button
        self.folder_nav_refresh_button = ttk.Button(
                                                    self.frame,
                                                    width=2,
                                                    text="R",
                                                    command=self.folderNavRefresh
                                                    )
        self.folder_nav_refresh_button.grid(column=0, row=0, sticky='w')

        # Folder path, entry
        self.folder_dir_entry = ttk.Entry(self.frame, textvariable=self.folder_dir)
        self.folder_dir_entry.grid(column=1, row=0, sticky='w'+'e')

        self.bindEntries()

    def folderDirGet(self, *args, **kwargs):
        return self.folder_dir.get()

    def bindEntries(self, *args, **kwargs):
        self.folder_dir_entry.bind('<Return>', self.openFolderTreeNav)

    def folderNavRefresh(self, *args, **kwargs):
        ''' Refreshes the folder navigation treeview '''
        folder_treeview.refreshView()
        inf_bar.lastActionRefresh('Refreshed Browse Files Treeview')

    def folderDirSet(self, *args, **kwargs):
        folder_path = fn_treeview.active_path
        self.folder_dir.set(folder_path)

    def openFolderTreeNav(self, *args, **kwags):
        ''' Loads the writen path to the file navigator treeview '''
        folder_path = self.folderDirGet()
        # Check if the path is a valid directory
        if os.path.isdir(folder_path):
            fn_treeview.refreshView(folder_path)
        else:
            inf_bar.lastActionRefresh('Not a Valid Directory')
            self.folderDirSet()


class ChangesNotebook:
    '''
        Draws the Notebook.
        It has the following pages:
            - Rename:
                Has the widgets to change the name of the selected files.
            - Metadata:
                Has the widgets to change the metadata of the selected files.
    '''
    def __init__(self, master, *args, **kwargs):
        # Create the notebook
        self.nb = ttk.Notebook(master)
        self.nb.grid(column=0, row=1)
        self.nb_rename = ttk.Frame(self.nb)
        self.nb_metadata = ttk.Frame(self.nb, padding='3 3 3 3')
        self.nb_metadata.columnconfigure(0, weight=1)

        # Add the rename page and call the widgets that go inside
        self.nb.add(self.nb_rename, text='Rename')
        self.renameNbPage(self.nb_rename)

        # Add the metadata page
        self.nb.add(self.nb_metadata, text='Metadata')
        # Call the widgets that go inside only if the modules were
        # installed and imported properly
        if METADATA_IMPORT:
            self.metadataNbPage(self.nb_metadata)
        else:
            self.nb.tab(1, state='disable')
            metadata_import_error_msg = ('No metadata modules available. This '
            'program is able to edit metadata tags if you install the mutagen '
            'and Pillow libraries')
            inf_bar.lastActionRefresh(metadata_import_error_msg)

        # Bindings
        self.bindEntries()

    def renameNbPage(self, master, *args, **kwargs):
        ''' Calls to draw the rename widgets '''
        self.nb_rename_frame = ttk.Frame(master)
        self.nb_rename_frame.grid(sticky='nsew')

        # Rename from File (0)
        self.rename_from_file = Rename_From_File(self.nb_rename_frame)
        # Regular Expressions (1)
        self.reg_exp = Reg_Exp(self.nb_rename_frame)
        # Name (2)
        self.name_basic = Name_Basic(self.nb_rename_frame)
        # Replace (3)
        self.replace = Replace(self.nb_rename_frame)
        # Case (4)
        self.case = Case(self.nb_rename_frame)
        # Remove (5)
        self.remove = Remove(self.nb_rename_frame)
        # Move/Copy Parts (6)
        self.move_copy_parts = Move_Copy_Parts(self.nb_rename_frame)
        # Add (7)
        self.add_to_string = Add_To_String(self.nb_rename_frame)
        # Append Folder Name (8)
        self.append_folder_name = Append_Folder_Name(self.nb_rename_frame)
        # Numbering (9)
        self.numbering = Numbering(self.nb_rename_frame)
        # Extension (10)
        self.extension_rep = Extension_Rep(self.nb_rename_frame)

        # Bottom Frame for Filters and Rename buttons
        self.nb_bottom_frame = ttk.Frame(self.nb_rename_frame)
        self.nb_bottom_frame.grid(column=0, row=3, columnspan=6, sticky='w'+'e')
        self.nb_bottom_frame.columnconfigure(0, weight=1)
        # Filters
        self.filters = Filters_Widget(self.nb_bottom_frame)
        # Rename
        self.rename = Rename(self.nb_bottom_frame)

        # Add a little bit of padding between each widget
        for child in self.nb_rename_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)

    def metadataNbPage(self, master, *args, **kwargs):
        ''' Calls to draw the matadata widgets '''
        self.nb_metadata_frame = ttk.Frame(master)
        self.nb_metadata_frame.grid(sticky='w'+'e')
        self.nb_metadata_frame.columnconfigure(0, weight=1)
        self.nb_metadata_frame.columnconfigure(1, weight=1)

        # Entries with the Metadata
        self.metadata_list_entries = Metadata_ListEntries(self.nb_metadata_frame)
        # Attached Image
        self.metadata_img = Metadata_Img(self.nb_metadata_frame)
        # Apply buttons
        self.apply_changes = Apply_Changes(self.nb_metadata_frame)

    def nbTabGet(self, *args, **kwargs):
        return self.nb.tab(self.nb.select(), "text")

    def bindEntries(self, *args, **kwargs):
        self.nb.bind('<<NotebookTabChanged>>', Populate_Fields)


class InfoBar:
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Frame(master)
        self.lf.grid(column=0, row=2, sticky='w'+'e')
        self.lf.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()
        self.numItemsRefresh()

        # Items, label
        self.items_label = ttk.Label(
                                        self.lf,
                                        textvariable=self.items_text_var,
                                        relief='sunken'
                                        )
        self.items_label.grid(column=0, row=0, ipadx=50, ipady=2, padx=4)

        # Last completed action, label
        self.action_label = ttk.Label(
                                        self.lf,
                                        textvariable=self.action_text_var,
                                        relief='sunken'
                                        )
        self.action_label.grid(column=1, row=0, sticky='w'+'e', ipady=2, padx=4)

    def numItemsRefresh(self, *args, **kwargs):
        num_items = len(fn_treeview.tree_folder.get_children())
        num_sel_items = len(fn_treeview.selectedItems())
        items_text = '{} items ({} selected)'.format(num_items, num_sel_items)
        self.items_text_var.set(items_text)

    def lastActionRefresh(self, action, *args, **kwargs):
        self.action_text_var.set(action)


###################################
'''
RENAME CLASSES
'''
###################################


class Rename_From_File:     # (0)
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Rename From File (0)')
        self.lf.grid(column=0, row=0, sticky='nsew')

        # Variable defs
        self.file = tk.StringVar()
        self.wrap = tk.BooleanVar()

        # Chose case, combobox
        ttk.Label(self.lf, text="Filename").grid(column=0, row=0, sticky='w')
        self.file_entry = ttk.Entry(
                                    self.lf,
                                    width=10,
                                    textvariable=self.file
                                    )
        self.file_entry.grid(column=1, row=0, sticky='ew')

        # Match case, checkbutton
        self.wrap_check = ttk.Checkbutton(
                                            self.lf,
                                            text='Wrap',
                                            variable=self.wrap,
                                            )
        self.wrap_check.grid(column=0, row=1)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=2, sticky='e', padx=2, pady=2)

        self.bindEntries()

    def fileGet(self, *args, **kwargs):
        return self.file.get()

    def wrapGet(self, *args, **kwargs):
        return self.wrap.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # Calls to update the new name column
        self.file.trace_add('write', fn_treeview.showNewName)
        self.wrap.trace_add('write', fn_treeview.showNewName)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.file.set('')
        self.wrap.set(False)

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.file.set(var_dict['rename_from_file_file'])
        self.wrap.set(var_dict['rename_from_file_wrap'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['rename_from_file_file'] = nb.rename_from_file.fileGet()
        dict_['rename_from_file_wrap'] = nb.rename_from_file.wrapGet()

    @staticmethod
    def Rename_From_File_Rename(name, idx, *wargs, **kwargs):
        '''
            Get the file to extract the names from, open it and match the names
            one to one per index base
        '''
        filename = nb.rename_from_file.fileGet()
        wrap = nb.rename_from_file.wrapGet()

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                lines = f.readlines()
                lines_count = len(lines)
                try:
                    if wrap:
                        name = lines[idx % lines_count]
                    else:
                        name = lines[idx]
                except IndexError:
                    pass
        return name


class Reg_Exp:  # (1)
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Regular Expressions (1)')
        self.lf.grid(column=1, row=0, sticky='nsew')

        # Variable defs
        self.match_reg = tk.StringVar()
        self.replace_with = tk.StringVar()

        # Match, entry
        ttk.Label(self.lf, text="Match").grid(column=0, row=0, sticky='w')
        self.match_reg_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.match_reg
                                            )
        self.match_reg_entry.grid(column=1, row=0, sticky='ew')

        # Replace with, entry
        ttk.Label(self.lf, text="Replace").grid(column=0, row=1, sticky='w')
        self.replace_with_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.replace_with
                                            )
        self.replace_with_entry.grid(column=1, row=1, sticky='ew')

        # Extended, button
        extended_button = ttk.Button(
                                        self.lf,
                                        text="Extend",
                                        command=self.extendedRegExp
                                        )
        extended_button.grid(column=1, row=2, sticky='w')

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=2, sticky='se', padx=2, pady=2)

        self.bindEntries()

    def matchRegGet(self, *args, **kwargs):
        return self.match_reg.get()

    def replaceWithGet(self, *args, **kwargs):
        return self.replace_with.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # Calls to update the new name column
        self.match_reg.trace_add('write', fn_treeview.showNewName)
        self.replace_with.trace_add('write', fn_treeview.showNewName)

    def extendedRegExp(self, *args, **kwargs):
        '''
            Create a pop up window with extended entries for the
            regular expressions and a button 'Done' that saves the changes
        '''
        self.ex_w_frame = tk.Toplevel(root, bg='gray85')
        self.ex_w_frame.title('Extended Regular Expression Window')
        self.ex_w_frame.attributes('-type', 'dialog')

        # Extended Match, text
        ttk.Label(self.ex_w_frame, text="Match").grid(column=0, row=0, sticky='w')
        self.ex_match_reg_text = tk.Text(
                                            self.ex_w_frame,
                                            bg='white',
                                            relief='sunken'
                                            )
        self.ex_match_reg_text.grid(column=0, row=1, sticky='ew')
        self.ex_match_reg_text.insert('end', self.matchRegGet())

        # Extended Replace, text
        ttk.Label(self.ex_w_frame, text="Replace").grid(column=0, row=2, sticky='w')
        self.ex_replace_with_text = tk.Text(
                                            self.ex_w_frame,
                                            bg='white',
                                            relief='sunken'
                                            )
        self.ex_replace_with_text.grid(column=0, row=3, sticky='ew')
        self.ex_replace_with_text.insert('end', self.replaceWithGet())

        # Close window, button
        self.done_button = ttk.Button(
                                        self.ex_w_frame,
                                        text="Done",
                                        command=self.saveExit
                                        )
        self.done_button.grid(column=0, row=4, sticky='e')

    def saveExit(self, *args, **kwargs):
        '''
            Gets the values of the text widgets and saves it to the variables.
            Then kills the window.
        '''
        ex_match_reg = self.ex_match_reg_text.get('1.0', 'end')
        ex_replace_with = self.ex_replace_with_text.get('1.0', 'end')

        # Remove the newline char
        ex_match_reg = ex_match_reg[:-1]
        ex_replace_with = ex_replace_with[:-1]

        # Save to variable
        self.match_reg.set(ex_match_reg)
        self.replace_with.set(ex_replace_with)

        # Kill window
        self.ex_w_frame.destroy()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.match_reg.set('')
        self.replace_with.set('')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.match_reg.set(var_dict['reg_exp_match_reg'])
        self.replace_with.set(var_dict['reg_exp_replace_with'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['reg_exp_match_reg'] = nb.reg_exp.matchRegGet()
        dict_['reg_exp_replace_with'] = nb.reg_exp.replaceWithGet()

    @staticmethod
    def Reg_Exp_Rename(name, *args, **kwargs):
        '''
            Matches the regular expression specified in the match_reg entry
            and recreates the name with the words and number groups specified
            in replace_with entry
            e.g:
                name: Program Files
                match_reg: ^([A-Z][a-z]*) ([A-Z][a-z]*)     # separates 2 words
                replace_with: The /2 which are used to run the /1

                returns: The Files which are used to run the Program
        '''
        match_reg = nb.reg_exp.matchRegGet()
        replace_with = nb.reg_exp.replaceWithGet()

        match_reg = re.compile(match_reg)
        reg_grouping = match_reg.match(name)
        if match_reg != '' and replace_with != '':
            for i in range(0, len(reg_grouping.groups()) + 1):
                n = str(i)

                # Prevent IndexError blocking
                try:
                    replace_with = replace_with.replace('/' + n,
                                                        reg_grouping.group(i))
                except IndexError:
                    pass

            name = replace_with

        return name


class Name_Basic:   # (2)
    '''
        Draws the Name widget. Inside the rename notebook. 2nd thing to change.
        It has:
            - A dropdown that lets you choose an option that affects
            the whole name
                - Keep: no change
                - Remove: compleatly erase the filename
                - Reverse: reverses the name, e.g. 12345.txt becomes 54321.txt
                - Fixed: specify a new name in the entry
            - An entry that lets you specify a name for all selected items
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Name (2)')
        self.lf.grid(column=2, row=0, sticky='nsew')

        # Variable defs
        self.name_opt = tk.StringVar()
        self.fixed_name = tk.StringVar()

        # Chose case, combobox
        ttk.Label(self.lf, text="Name").grid(column=0, row=0, sticky='w')
        self.name_opt_combo = ttk.Combobox(
                                            self.lf,
                                            width=10,
                                            state='readonly',
                                            values=('Keep', 'Remove',
                                                    'Reverse', 'Fixed'),
                                            textvariable=self.name_opt
                                            )
        self.name_opt_combo.grid(column=1, row=0, sticky='ew')
        self.name_opt_combo.current(0)

        # Replace this, entry
        self.fixed_name_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.fixed_name
                                            )
        self.fixed_name_entry.grid(column=1, row=1, sticky='ew')

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=2, sticky='e', padx=2, pady=2)

        self.bindEntries()

    def nameOptGet(self, *args, **kwargs):
        return self.name_opt.get()

    def fixedNameGet(self, *args, **kwargs):
        return self.fixed_name.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.name_opt_combo.bind('<<ComboboxSelected>>', self.defocus)

        # Calls to update the new name column
        self.name_opt.trace_add('write', fn_treeview.showNewName)
        self.fixed_name.trace_add('write', fn_treeview.showNewName)

    def defocus(self, event=None, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.name_opt_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.name_opt.set('Keep')
        self.fixed_name.set('')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.name_opt.set(var_dict['name_basic_name_opt'])
        self.fixed_name.set(var_dict['name_basic_fixed_name'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['name_basic_name_opt'] = nb.name_basic.nameOptGet()
        dict_['name_basic_fixed_name'] = nb.name_basic.fixedNameGet()

    @staticmethod
    def Name_Basic_Rename(name, *args, **kwargs):
        ''' Self explanatory '''
        name_opt = nb.name_basic.nameOptGet()

        if name_opt == 'Remove':
            name = ''
        elif name_opt == 'Reverse':
            name = name[::-1]
        elif name_opt == 'Fixed':
            name = nb.name_basic.fixedNameGet()

        return name


class Replace:  # (3)
    '''
        Draws the replace widget. Inside rename notebook. 3rd thing to change.
        It has:
            - Entry to choose char(s) to replace
            - Entry for what to replace those char(s) with
            - Reset button
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Replace (3)')
        self.lf.grid(column=1, row=1, columnspan=2, sticky='nsew')

        # Variable defs
        self.replace_this = tk.StringVar()
        self.replace_with = tk.StringVar()
        self.match_case = tk.BooleanVar()

        # Replace this, entry
        ttk.Label(self.lf, text="Replace").grid(column=0, row=0, sticky='w')
        self.replace_this_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.replace_this
                                            )
        self.replace_this_entry.grid(column=1, row=0, sticky='ew')

        # Replace with, entry
        ttk.Label(self.lf, text="With").grid(column=0, row=1, sticky='w')
        self.replace_with_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.replace_with
                                            )
        self.replace_with_entry.grid(column=1, row=1, sticky='ew')

        # Match case, checkbutton
        self.match_case_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Match Case',
                                                variable=self.match_case,
                                                )
        self.match_case_check.grid(column=0, row=2)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=2, sticky='e', padx=2, pady=2)

        self.bindEntries()

    def replaceThisGet(self, *args, **kwargs):
        return self.replace_this.get()

    def replaceWithGet(self, *args, **kwargs):
        return self.replace_with.get()

    def matchCaseGet(self, *args, **kwargs):
        return self.match_case.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # Calls to update the new name column
        self.replace_this.trace_add('write', fn_treeview.showNewName)
        self.replace_with.trace_add('write', fn_treeview.showNewName)
        self.match_case.trace_add('write', fn_treeview.showNewName)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.replace_this.set('')
        self.replace_with.set('')
        self.match_case.set(False)

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.replace_this.set(var_dict['replace_replace_this'])
        self.replace_with.set(var_dict['replace_replace_with'])
        self.match_case.set(var_dict['replace_match_case'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['replace_replace_this'] = nb.replace.replaceThisGet()
        dict_['replace_replace_with'] = nb.replace.replaceWithGet()
        dict_['replace_match_case'] = nb.replace.matchCaseGet()

    @staticmethod
    def Replace_Action(name, *args, **kwargs):
        ''' Does the replace action for the new name '''
        replace_this = nb.replace.replaceThisGet()
        replace_with = nb.replace.replaceWithGet()
        match_case = nb.replace.matchCaseGet()

        # When replacing with match case it's a simple matter
        if match_case:
            name = name.replace(replace_this, replace_with)
        # But when replacing without minding the case...
        # (If replace_this is empty it breaks)
        elif replace_this != '':
            # Start searching from the start of the string
            idx = 0
            while True:
                # Find at what position what we want to replace is
                # (all in lowercase)
                idx = name.lower().find(replace_this.lower(), idx)
                # If find returns a -1 it means it didn't find it and we can
                # break out of the loop
                if idx == -1:
                    break

                # Create the new name
                name = (name[:idx] + replace_with +
                        name[idx + len(replace_this):])

                # New index from where to search
                idx = idx + len(replace_with)

        return name


class Case:     # (4)
    '''
        Draws the Case changer widget. Inside rename notebook.
        4th thing to change.
        It has:
            - Combobox to choose what case to use (same, upper, lower, title)
            - Reset button
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Case (4)')
        self.lf.grid(column=0, row=1, sticky='nsew')

        # Variable defs
        self.case_want = tk.StringVar()

        # Chose case, combobox
        ttk.Label(self.lf, text="Case").grid(column=0, row=0, sticky='w')
        self.case_combo = ttk.Combobox(
                                        self.lf,
                                        width=10,
                                        state='readonly',
                                        values=('Same', 'Upper Case',
                                                'Lower Case', 'Title',
                                                'Sentence'),
                                        textvariable=self.case_want
                                        )
        self.case_combo.grid(column=1, row=0, sticky='ew')
        self.case_combo.current(0)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=1, sticky='e', padx=2, pady=2)

        self.bindEntries()

    def caseWantGet(self, *args, **kwargs):
        return self.case_want.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.case_combo.bind('<<ComboboxSelected>>', self.defocus)

        # Calls to update the new name column
        self.case_want.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.case_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.case_want.set('Same')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.case_want.set(var_dict['case_case_want'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['case_case_want'] = nb.case.caseWantGet()

    @staticmethod
    def Case_Change(name, *args, **kwargs):
        ''' Does the case change for the new name '''
        case_want = nb.case.caseWantGet()

        if case_want == 'Upper Case':
            name = name.upper()

        elif case_want == 'Lower Case':
            name = name.lower()

        elif case_want == 'Title':
            name = name.title()

        elif case_want == 'Sentence':
            name = name.capitalize()

        return name


class Remove:   # (5)
    '''
        Draws the Remove widget. Inside rename notebook. 5th thing to change.
        It has:
            - ttk.Spinbox to remove the first n char(s)
            - ttk.Spinbox to remove the last n char(s)
            - ttk.Spinbox to choose what char to remove from
            - ttk.Spinbox to choose what char to remove up to
            - Entry for char(s) to remove
            - Entry for word(s) to remove
            - Combobox to crop (before, after)
            - Entry for what to remove before/after
            - Checkbutton to remove digits
            - Checkbutton to remove D/S
            - Checkbutton to remove accents
            - Checkbutton to remove chars
            - Checkbutton to remove sym
            - Combobox to remove lead dots (None,...)
            - Reset button
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Remove (5)')
        self.lf.grid(column=3, row=0, rowspan=2, sticky='nsew')

        # Variable defs
        self.first_n = tk.IntVar()
        self.last_n = tk.IntVar()
        self.from_n = tk.IntVar()
        self.to_n = tk.IntVar()
        self.rm_words = tk.StringVar()
        self.rm_chars = tk.StringVar()
        self.crop_pos = tk.StringVar()
        self.crop_this = tk.StringVar()
        self.digits = tk.BooleanVar()
        self.d_s = tk.BooleanVar()
        self.accents = tk.BooleanVar()
        self.chars = tk.BooleanVar()
        self.sym = tk.BooleanVar()
        self.lead_dots = tk.StringVar()

        # Remove first n characters, spinbox
        ttk.Label(self.lf, text='First n').grid(column=0, row=0, sticky='ew')
        self.first_n_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.first_n
                                        )
        self.first_n_spin.grid(column=1, row=0)

        # Remove las n characters, spinbox
        ttk.Label(self.lf, text='Last n').grid(column=2, row=0, sticky='ew')
        self.last_n_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.last_n
                                        )
        self.last_n_spin.grid(column=3, row=0)

        # Remove from this char position, spinbox
        ttk.Label(self.lf, text='From').grid(column=0, row=1, sticky='ew')
        self.from_n_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.from_n
                                        )
        self.from_n_spin.grid(column=1, row=1)

        # Remove to this char position, spinbox
        ttk.Label(self.lf, text='To').grid(column=2, row=1, sticky='ew')
        self.to_n_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.to_n
                                        )
        self.to_n_spin.grid(column=3, row=1)

        # Remove word(s), entry
        ttk.Label(self.lf, text='Words').grid(column=0, row=2, sticky='ew')
        self.rm_words_entry = ttk.Entry(
                                        self.lf,
                                        width=5,
                                        textvariable=self.rm_words
                                        )
        self.rm_words_entry.grid(column=1, row=2, sticky='ew')

        # Remove character(s), entry
        ttk.Label(self.lf, text='Chars').grid(column=2, row=2, sticky='ew')
        self.rm_chars_entry = ttk.Entry(
                                        self.lf,
                                        width=5,
                                        textvariable=self.rm_chars
                                        )
        self.rm_chars_entry.grid(column=3, row=2, sticky='ew')

        # Choose where to crop, combobox
        ttk.Label(self.lf, text="Crop").grid(column=0, row=3, sticky='w')
        self.crop_combo = ttk.Combobox(
                                        self.lf,
                                        width=5,
                                        state='readonly',
                                        values=('Before', 'After', 'Special'),
                                        textvariable=self.crop_pos
                                        )
        self.crop_combo.grid(column=1, row=3, sticky='ew')
        self.crop_combo.current(0)

        # Crop, entry
        self.crop_this_entry = ttk.Entry(
                                            self.lf,
                                            width=5,
                                            textvariable=self.crop_this
                                            )
        self.crop_this_entry.grid(column=2, row=3, columnspan=2, sticky='ew')

        # Remove digits, checkbutton
        self.digits_check = ttk.Checkbutton(
                                            self.lf,
                                            text='Digits',
                                            variable=self.digits,
                                            )
        self.digits_check.grid(column=0, row=4)

        # Remove chars, checkbutton
        self.chars_check = ttk.Checkbutton(
                                            self.lf,
                                            text='Chars',
                                            variable=self.chars,
                                            )
        self.chars_check.grid(column=1, row=4)

        # Remove sym, checkbutton
        self.sym_check = ttk.Checkbutton(
                                            self.lf,
                                            text='Sym.',
                                            variable=self.sym,
                                            )
        self.sym_check.grid(column=2, row=4)

        # Remove D/S, checkbutton
        self.d_s_check = ttk.Checkbutton(
                                            self.lf,
                                            text='D/S',
                                            variable=self.d_s,
                                            )
        self.d_s_check.grid(column=0, row=5)

        # Remove accents, checkbutton
        self.accents_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Accents',
                                                variable=self.accents,
                                                )
        self.accents_check.grid(column=1, row=5)

        # Remove Leading Dots, combobox
        ttk.Label(self.lf, text="Lead Dots").grid(column=0, row=6, sticky='w')
        self.lead_dots_combo = ttk.Combobox(
                                            self.lf,
                                            width=5,
                                            state='readonly',
                                            values=('None', '.', '..'),
                                            textvariable=self.lead_dots
                                            )
        self.lead_dots_combo.grid(column=1, row=6, sticky='ew')
        self.lead_dots_combo.current(0)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=20, row=20, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def firstNGet(self, *args, **kwargs):
        return self.first_n.get()

    def lastNGet(self, *args, **kwargs):
        return self.last_n.get()

    def fromNGet(self, *args, **kwargs):
        return self.from_n.get()

    def toNGet(self, *args, **kwargs):
        return self.to_n.get()

    def rmWordsGet(self, *args, **kwargs):
        return self.rm_words.get()

    def rmCharsGet(self, *args, **kwargs):
        return self.rm_chars.get()

    def cropPosGet(self, *args, **kwargs):
        return self.crop_pos.get()

    def cropThisGet(self, *args, **kwargs):
        return self.crop_this.get()

    def digitsGet(self, *args, **kwargs):
        return self.digits.get()

    def d_sGet(self, *args, **kwargs):
        return self.d_s.get()

    def accentsGet(self, *args, **kwargs):
        return self.accents.get()

    def charsGet(self, *args, **kwargs):
        return self.chars.get()

    def symGet(self, *args, **kwargs):
        return self.sym.get()

    def leadDotsGet(self, *args, **kwargs):
        return self.lead_dots.get()

    def bindEntries(self, *args, **kwargs):
        ''' What to execute when the bindings happen. '''
        # When updating from_n value makes sure its not bigger than to_n
        self.from_n.trace_add('write', self.fromAddTo)
        self.to_n.trace_add('write', self.fromAddTo)
        # Defocus the hightlight when changing combobox
        self.lead_dots_combo.bind('<<ComboboxSelected>>', self.defocus)
        self.crop_combo.bind('<<ComboboxSelected>>', self.defocus)

        # Calls to update the new name column
        self.first_n.trace_add('write', fn_treeview.showNewName)
        self.last_n.trace_add('write', fn_treeview.showNewName)
        self.from_n.trace_add('write', fn_treeview.showNewName)
        self.to_n.trace_add('write', fn_treeview.showNewName)
        self.rm_words.trace_add('write', fn_treeview.showNewName)
        self.rm_chars.trace_add('write', fn_treeview.showNewName)
        self.crop_pos.trace_add('write', fn_treeview.showNewName)
        self.crop_this.trace_add('write', fn_treeview.showNewName)
        self.digits.trace_add('write', fn_treeview.showNewName)
        self.d_s.trace_add('write', fn_treeview.showNewName)
        self.accents.trace_add('write', fn_treeview.showNewName)
        self.chars.trace_add('write', fn_treeview.showNewName)
        self.sym.trace_add('write', fn_treeview.showNewName)
        self.lead_dots.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.lead_dots_combo.selection_clear()
        self.crop_combo.selection_clear()

    def fromAddTo(self, *args, **kwargs):
        '''
            Checks if the from_n value is bigger than the to_n value,
            If so raises the to_n value accordingly.
        '''
        a = self.fromNGet()
        b = self.toNGet()

        if a > b:
            self.to_n.set(a)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget. '''
        self.first_n.set(0)
        self.last_n.set(0)
        self.from_n.set(0)
        self.to_n.set(0)
        self.rm_words.set('')
        self.rm_chars.set('')
        self.crop_pos.set('Before')
        self.crop_this.set('')
        self.digits.set(False)
        self.d_s.set(False)
        self.accents.set(False)
        self.chars.set(False)
        self.sym.set(False)
        self.lead_dots.set('None')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.first_n.set(var_dict['remove_first_n'])
        self.last_n.set(var_dict['remove_last_n'])
        self.from_n.set(var_dict['remove_from_n'])
        self.to_n.set(var_dict['remove_to_n'])
        self.rm_words.set(var_dict['remove_rm_words'])
        self.rm_chars.set(var_dict['remove_rm_chars'])
        self.crop_pos.set(var_dict['remove_crop_pos'])
        self.crop_this.set(var_dict['remove_crop_this'])
        self.digits.set(var_dict['remove_digits'])
        self.d_s.set(var_dict['remove_d_s'])
        self.accents.set(var_dict['remove_accents'])
        self.chars.set(var_dict['remove_chars'])
        self.sym.set(var_dict['remove_sym'])
        self.lead_dots.set(var_dict['remove_lead_dots'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['remove_first_n'] = nb.remove.firstNGet()
        dict_['remove_last_n'] = nb.remove.lastNGet()
        dict_['remove_from_n'] = nb.remove.fromNGet()
        dict_['remove_to_n'] = nb.remove.toNGet()
        dict_['remove_rm_words'] = nb.remove.rmWordsGet()
        dict_['remove_rm_chars'] = nb.remove.rmCharsGet()
        dict_['remove_crop_pos'] = nb.remove.cropPosGet()
        dict_['remove_crop_this'] = nb.remove.cropThisGet()
        dict_['remove_digits'] = nb.remove.digitsGet()
        dict_['remove_d_s'] = nb.remove.d_sGet()
        dict_['remove_accents'] = nb.remove.accentsGet()
        dict_['remove_chars'] = nb.remove.charsGet()
        dict_['remove_sym'] = nb.remove.symGet()
        dict_['remove_lead_dots'] = nb.remove.leadDotsGet()

    @staticmethod
    def Remove_N_Chars(name, *args, **kwargs):
        ''' Removes chars depending on their index '''
        first_n = nb.remove.firstNGet()
        # Need this to be a negative number
        last_n = -nb.remove.lastNGet()
        # Need this to be one less of the displayed number
        from_n = nb.remove.fromNGet() - 1
        to_n = nb.remove.toNGet()

        name = name[first_n:]
        # Only act when the index is not 0
        if last_n != 0:
            name = name[:last_n]
        # Only act when the index is not -1
        if from_n != -1:
            # Doing it with str slices is faster than transforming it to a list
            name = name[:from_n] + name[to_n:]

        return name

    @staticmethod
    def Remove_Words_Chars(name, *args, **kwargs):
        '''
            Firstly removes the apparition of a word (must be between spaces).
            Secondly removes every apparition of any of the chars that were
            input in the entry.
        '''
        rm_words = nb.remove.rmWordsGet()
        rm_chars = nb.remove.rmCharsGet()

        # removes the words first
        name = name.split()

        # If the value doesnt exist it raises a ValueError
        try:
            # Needs the while to remove all ocurences of the word
            while rm_words in name:
                name.remove(rm_words)
        except ValueError:
            pass
        name = ' '.join(name)

        # Removes every apparition of all chars in the str by themselves
        for chara in rm_chars:
            name = name.replace(chara, '')

        return name

    @staticmethod
    def Crop_Remove(name, *args, **kwargs):
        '''
            Crops before or after the specified char(s).
            It can also crop inbetween 2 char(s), ex:
            a*b (for cropping between the first ocurrence of a and b)
            \[*\] (for cropping between [ and ])
        '''
        crop_pos = nb.remove.cropPosGet()
        crop_this = nb.remove.cropThisGet()

        # If this field is empty do nothing
        if crop_this != '':
            # If the combobox is not in 'Special' do the regular crops
            if crop_pos != 'Special':
                name_tuple = name.partition(crop_this)
                if crop_pos == 'Before':
                    name = name_tuple[2]
                elif crop_pos == 'After':
                    name = name_tuple[0]
            else:
                # Create a regular expresion from the given string
                reg_exp = crop_this.replace('*', '.+?', 1)
                reg_exp = re.compile(reg_exp)
                name = re.sub(reg_exp, '', name)

        return name

    @staticmethod
    def Remove_Checkbuttons(name, *args, **kwargs):
        ''' Checks what checkbuttons are active and removes accordingly '''
        digits = nb.remove.digitsGet()
        d_s = nb.remove.d_sGet()
        accents = nb.remove.accentsGet()
        chars = nb.remove.charsGet()
        sym = nb.remove.symGet()

        if digits:
            for char in string.digits:
                name = name.replace(char, '')
        if d_s:
            name = name.replace('  ', ' ')
        if accents:     # not sure how this bit works (from stackoverflow)
            nfkd_form = unicodedata.normalize('NFKD', name)
            name = ''.join(
                [c for c in nfkd_form if not unicodedata.combining(c)]
                )
        if chars:
            for char in string.ascii_letters:
                name = name.replace(char, '')
        if sym:
            for char in string.punctuation:
                name = name.replace(char, '')

        return name

    @staticmethod
    def Lead_Dots(name, *args, **kwargs):
        ''' Removes either '.' or '..' right at the begining '''
        lead_dots = nb.remove.leadDotsGet()
        if lead_dots != 'None':
            name = name.replace(lead_dots, '', 1)

        return name

    @staticmethod
    def Remove_Rename(name, *args, **kwargs):
        ''' Main remove function. It's been broken down into simpler parts '''
        name = Remove.Remove_N_Chars(name)
        name = Remove.Remove_Words_Chars(name)
        name = Remove.Crop_Remove(name)
        name = Remove.Remove_Checkbuttons(name)
        name = Remove.Lead_Dots(name)

        return name


class Move_Copy_Parts:  # (6)
    '''
        Draws the move/copy parts widget. Inside rename notebook.
        6th thing to change.
        It has:
            - Combobox to select where to select the text from (start, end)
            - ttk.Spinbox to select how many characters to select
            - Combobox to select where to paste the char(s) to
            (start, end, position)
            - ttk.Spinbox to select where to paste when 'position' is selected
            - Entry to write a separator
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Move/Copy Parts (6)')
        self.lf.grid(column=0, row=2, columnspan=3, sticky='nsew')

        # Variable defs
        self.ori_pos = tk.StringVar()
        self.ori_n = tk.IntVar()
        self.end_pos = tk.StringVar()
        self.end_n = tk.IntVar()
        self.sep = tk.StringVar()

        # Copy from, combobox
        ttk.Label(self.lf, text="Copy").grid(column=0, row=0)
        self.ori_pos_combo = ttk.Combobox(
                                            self.lf,
                                            width=5,
                                            state='readonly',
                                            values=('None', 'Start', 'End'),
                                            textvariable=self.ori_pos
                                            )
        self.ori_pos_combo.grid(column=1, row=0, sticky='ew')
        self.ori_pos_combo.current(0)

        # Copy n characters, spinbox
        ttk.Label(self.lf, text="Chars").grid(column=2, row=0)
        self.ori_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.ori_n
                                    )
        self.ori_n_spin.grid(column=3, row=0)

        # Paste to, combobox
        ttk.Label(self.lf, text="Paste").grid(column=4, row=0)
        self.end_pos_combo = ttk.Combobox(
                                        self.lf,
                                        width=5,
                                        state='readonly',
                                        values=('Start', 'End', 'Position'),
                                        textvariable=self.end_pos
                                        )
        self.end_pos_combo.grid(column=5, row=0, sticky='ew')
        self.end_pos_combo.current(0)

        # Paste in n position, spinbox
        ttk.Label(self.lf, text="Pos").grid(column=6, row=0)
        self.end_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.end_n
                                    )
        self.end_n_spin.grid(column=7, row=0)

        # Separator between pasted part and position, entry
        ttk.Label(self.lf, text='Sep.').grid(column=8, row=0)
        self.sep_entry = ttk.Entry(
                                    self.lf,
                                    width=5,
                                    textvariable=self.sep
                                    )
        self.sep_entry.grid(column=9, row=0)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=10, row=1, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def oriPosGet(self, *args, **kwargs):
        return self.ori_pos.get()

    def oriNGet(self, *args, **kwargs):
        return self.ori_n.get()

    def endPosGet(self, *args, **kwargs):
        return self.end_pos.get()

    def endNGet(self, *args, **kwargs):
        return self.end_n.get()

    def sepGet(self, *args, **kwargs):
        return self.sep.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.ori_n.trace_add('write', self.fromAddTo)
        self.end_n.trace_add('write', self.fromAddTo)
        self.ori_pos_combo.bind('<<ComboboxSelected>>', self.defocus)
        self.end_pos_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.ori_pos.trace_add('write', fn_treeview.showNewName)
        self.ori_n.trace_add('write', fn_treeview.showNewName)
        self.end_pos.trace_add('write', fn_treeview.showNewName)
        self.end_n.trace_add('write', fn_treeview.showNewName)
        self.sep.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.ori_pos_combo.selection_clear()
        self.end_pos_combo.selection_clear()

    def fromAddTo(self, *args, **kwargs):
        '''
            Checks if the from_n value is bigger than the to_n value,
            If so raises the to_n value accordingly.
        '''
        a = self.oriNGet()
        b = self.endNGet()

        if a > b:
            self.end_n.set(a)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.ori_pos.set('None')
        self.ori_n.set(0)
        self.end_pos.set('Start')
        self.end_n.set(0)
        self.sep.set('')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.ori_pos.set(var_dict['move_copy_parts_ori_pos'])
        self.ori_n.set(var_dict['move_copy_parts_ori_n'])
        self.end_pos.set(var_dict['move_copy_parts_end_pos'])
        self.end_n.set(var_dict['move_copy_parts_end_n'])
        self.sep.set(var_dict['move_copy_parts_sep'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['move_copy_parts_ori_pos'] = nb.move_copy_parts.oriPosGet()
        dict_['move_copy_parts_ori_n'] = nb.move_copy_parts.oriNGet()
        dict_['move_copy_parts_end_pos'] = nb.move_copy_parts.endPosGet()
        dict_['move_copy_parts_end_n'] = nb.move_copy_parts.endNGet()
        dict_['move_copy_parts_sep'] = nb.move_copy_parts.sepGet()

    @staticmethod
    def Move_Copy_Action(name, *args, **kwargs):
        '''
            Copies and pastes the selected characters to the selected
            position.
        '''
        ori_pos = nb.move_copy_parts.oriPosGet()
        ori_n = nb.move_copy_parts.oriNGet()
        end_pos = nb.move_copy_parts.endPosGet()
        end_n = nb.move_copy_parts.endNGet()
        sep = nb.move_copy_parts.sepGet()

        if ori_pos == 'Start':
            if end_pos == 'End':
                name = name[ori_n:] + sep + name[:ori_n]

            elif end_pos == 'Position':
                name = (name[ori_n:end_n] + sep +
                        name[:ori_n] + sep + name[end_n:])

        elif ori_pos == 'End':
            if end_pos == 'Start':
                name = name[-ori_n:] + sep + name[:-ori_n]

            elif end_pos == 'Position':
                name = (name[:end_n] + sep +
                        name[-ori_n:] + sep + name[end_n:-ori_n])

        return name


class Add_To_String:    # (7)
    '''
        Draws the Add widget. Inside the rename notebook. 7th thing to change.
        It has:
            - A prefix entry that adds the char(s) as a prefix
            - An insert entry that at adds the char(s) at the specified pos
            - A at pos spinbox that specifies the position to insert
            the char(s)
            - A suffix entry that adds the char(s) as a suffix
            - A word space checkbox that adds a space before each capital
            letter
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Add (7)')
        self.lf.grid(column=4, row=0, rowspan=2, sticky='nsew')

        # Variable defs
        self.prefix = tk.StringVar()
        self.insert_this = tk.StringVar()
        self.at_pos = tk.IntVar()
        self.suffix = tk.StringVar()
        self.word_space = tk.BooleanVar()

        # Prefix, entry
        ttk.Label(self.lf, text='Prefix').grid(column=0, row=0, sticky='ew')
        self.prefix_entry = ttk.Entry(
                                        self.lf,
                                        width=5,
                                        textvariable=self.prefix
                                        )
        self.prefix_entry.grid(column=1, row=0, sticky='ew')

        # Insert, entry
        ttk.Label(self.lf, text='Insert').grid(column=0, row=1, sticky='ew')
        self.insert_this_entry = ttk.Entry(
                                            self.lf,
                                            width=5,
                                            textvariable=self.insert_this
                                            )
        self.insert_this_entry.grid(column=1, row=1, sticky='ew')

        # Insert char(s) at position, spinbox
        ttk.Label(self.lf, text='At pos.').grid(column=0, row=2, sticky='ew')
        self.at_pos_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    from_=-MAX_NAME_LEN,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.at_pos
                                    )
        self.at_pos_spin.grid(column=1, row=2)
        self.at_pos.set(0)

        # Suffix, entry
        ttk.Label(self.lf, text='Suffix').grid(column=0, row=3, sticky='ew')
        self.suffix_entry = ttk.Entry(
                                        self.lf,
                                        width=5,
                                        textvariable=self.suffix
                                        )
        self.suffix_entry.grid(column=1, row=3, sticky='ew')

        # Word space, checkbutton
        self.word_space_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Word Space',
                                                variable=self.word_space
                                                )
        self.word_space_check.grid(column=0, row=4)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=20, row=20, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def prefixGet(self, *args, **kwargs):
        return self.prefix.get()

    def insertThisGet(self, *args, **kwargs):
        return self.insert_this.get()

    def atPosGet(self, *args, **kwargs):
        return self.at_pos.get()

    def suffixGet(self, *args, **kwargs):
        return self.suffix.get()

    def wordSpaceGet(self, *args, **kwargs):
        return self.word_space.get()

    def bindEntries(self, *args, **kwargs):
        ''' What to execute when the bindings happen. '''
        # calls to update the new name column
        self.prefix.trace_add('write', fn_treeview.showNewName)
        self.insert_this.trace_add('write', fn_treeview.showNewName)
        self.at_pos.trace_add('write', fn_treeview.showNewName)
        self.suffix.trace_add('write', fn_treeview.showNewName)
        self.word_space.trace_add('write', fn_treeview.showNewName)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget. '''
        self.prefix.set('')
        self.insert_this.set('')
        self.at_pos.set(0)
        self.suffix.set('')
        self.word_space.set(False)

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.prefix.set(var_dict['add_to_string_prefix'])
        self.insert_this.set(var_dict['add_to_string_insert_this'])
        self.at_pos.set(var_dict['add_to_string_at_pos'])
        self.suffix.set(var_dict['add_to_string_suffix'])
        self.word_space.set(var_dict['add_to_string_word_space'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['add_to_string_prefix'] = nb.add_to_string.prefixGet()
        dict_['add_to_string_insert_this'] = nb.add_to_string.insertThisGet()
        dict_['add_to_string_at_pos'] = nb.add_to_string.atPosGet()
        dict_['add_to_string_suffix'] = nb.add_to_string.suffixGet()
        dict_['add_to_string_word_space'] = nb.add_to_string.wordSpaceGet()

    @staticmethod
    def Add_Rename(name, *args, **kwargs):
        '''
            Adds the char(s) to the specified position.
            Also can add spaces before capital letters.
        '''
        prefix = nb.add_to_string.prefixGet()
        insert_this = nb.add_to_string.insertThisGet()
        at_pos = nb.add_to_string.atPosGet()
        suffix = nb.add_to_string.suffixGet()
        word_space = nb.add_to_string.wordSpaceGet()

        name = prefix + name
        name = name[:at_pos] + insert_this + name[at_pos:]
        name = name + suffix

        if word_space:  # add a space before each capital letter
            name = ''.join([' ' + ch if ch.isupper() else ch for ch in name])

        return name


class Append_Folder_Name:   # (8)
    '''
        Draws the Append Folder Name. Inside the rename notebook. 8th thing to
        change.
        It has:
            - Dropdown that lets you choose position
            - Entry that lets you specify a separator
            - ttk.Spinbox that lets you choose how many folder levels to add
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Append Folder Name (8)')
        self.lf.grid(column=3, row=2, columnspan=2, sticky='nsew')

        # Variable defs
        self.name_pos = tk.StringVar()
        self.sep = tk.StringVar()
        self.levels = tk.IntVar()

        # Name, combobox
        ttk.Label(self.lf, text='Name').grid(column=0, row=0, sticky='ew')
        self.name_pos_combo = ttk.Combobox(
                                        self.lf,
                                        width=5,
                                        state='readonly',
                                        values=('Prefix', 'Suffix'),
                                        textvariable=self.name_pos
                                        )
        self.name_pos_combo.grid(column=1, row=0, sticky='ew')
        self.name_pos_combo.current(0)

        # Separator, entry
        ttk.Label(self.lf, text='Sep.').grid(column=2, row=0, sticky='ew')
        self.sep_entry = ttk.Entry(
                                    self.lf,
                                    width=5,
                                    textvariable=self.sep
                                    )
        self.sep_entry.grid(column=3, row=0, sticky='ew')

        # Folders levels, spinbox
        ttk.Label(self.lf, text='Levels').grid(column=4, row=0, sticky='ew')
        self.levels_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    from_=0,
                                    to=500,
                                    textvariable=self.levels
                                    )
        self.levels_spin.grid(column=5, row=0)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=20, row=20, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def namePosGet(self, *args, **kwargs):
        return self.name_pos.get()

    def sepGet(self, *args, **kwargs):
        return self.sep.get()

    def levelsGet(self, *args, **kwargs):
        return self.levels.get()

    def bindEntries(self, *args, **kwargs):
        ''' What to execute when the bindings happen. '''
        # Defocus the hightlight when changing combobox
        self.name_pos_combo.bind('<<ComboboxSelected>>', self.defocus)

        # Calls to update the new name column
        self.name_pos.trace_add('write', fn_treeview.showNewName)
        self.sep.trace_add('write', fn_treeview.showNewName)
        self.levels.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.name_pos_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget. '''
        self.name_pos.set('Prefix')
        self.sep.set('')
        self.levels.set(0)

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.name_pos.set(var_dict['append_folder_name_name_pos'])
        self.sep.set(var_dict['append_folder_name_sep'])
        self.levels.set(var_dict['append_folder_name_levels'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['append_folder_name_name_pos'] = nb.append_folder_name.namePosGet()
        dict_['append_folder_name_sep'] = nb.append_folder_name.sepGet()
        dict_['append_folder_name_levels'] = nb.append_folder_name.levelsGet()

    @staticmethod
    def Append_Folder_Rename(name, path, *args, **kwargs):
        name_pos = nb.append_folder_name.namePosGet()
        sep = nb.append_folder_name.sepGet()
        levels = nb.append_folder_name.levelsGet()

        folders = path.split('/')
        folder_full = ''
        for i in range(2, levels + 2):
            folder_full = folders[-i] + sep + folder_full

        if name_pos == 'Prefix':
            name = folder_full + name
        elif name_pos == 'Suffix':
            name = name + sep + folder_full
            if sep:
                # Remove the extra trailing separator
                name = name[:-len(sep)]

        return name


class Numbering:    # (9)
    '''
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
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Numbering (9)')
        self.lf.grid(column=5, row=0, rowspan=2, sticky='nsew')

        # Variable defs
        self.mode = tk.StringVar()
        self.at_n = tk.IntVar()
        self.start_num = tk.IntVar()
        self.incr_num = tk.IntVar(value=1)
        self.pad = tk.IntVar(value=1)
        self.sep = tk.StringVar()
        self.type_base = tk.StringVar()

        # Mode, combobox
        ttk.Label(self.lf, text='Mode').grid(column=0, row=0, sticky='ew')
        self.mode_combo = ttk.Combobox(
                                        self.lf,
                                        width=5,
                                        state='readonly',
                                        values=('None', 'Prefix', 'Suffix',
                                                'Both', 'Position'),
                                        textvariable=self.mode
                                        )
        self.mode_combo.grid(column=1, row=0, sticky='ew')
        self.mode_combo.current(0)

        # At position, spinbox
        ttk.Label(self.lf, text='at').grid(column=2, row=0, sticky='ew')
        self.at_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    from_=-MAX_NAME_LEN,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.at_n
                                    )
        self.at_n_spin.grid(column=3, row=0)

        # Start from this number, spinbox
        ttk.Label(self.lf, text='Start').grid(column=0, row=1, sticky='ew')
        self.start_num_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.start_num
                                        )
        self.start_num_spin.grid(column=1, row=1)

        # Step, spinbox
        ttk.Label(self.lf, text='Incr.').grid(column=2, row=1, sticky='ew')
        self.incr_num_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        from_=1,
                                        to=MAX_NAME_LEN,
                                        textvariable=self.incr_num
                                        )
        self.incr_num_spin.grid(column=3, row=1)
        # TKINTER BUG
        # The ttk.spinbox doesn't begin in the minimun value thats set
        # Solution would be to set it to the desired number as initialization
        # But this is not a bug from my end

        # Padding of possible 0s, spinbox
        ttk.Label(self.lf, text='Pad').grid(column=0, row=2, sticky='ew')
        self.pad_spin = ttk.Spinbox(
                                self.lf,
                                width=3,
                                from_=1,
                                to=MAX_NAME_LEN,
                                textvariable=self.pad
                                )
        self.pad_spin.grid(column=1, row=2)
        # TKINTER BUG
        # The ttk.spinbox doesn't begin in the minimun value thats set
        # Solution would be to set it to the desired number as initialization
        # But this is not a bug from my end

        # Separator, entry
        ttk.Label(self.lf, text='Sep.').grid(column=2, row=2, sticky='ew')
        self.sep_entry = ttk.Entry(
                                    self.lf,
                                    width=5,
                                    textvariable=self.sep
                                    )
        self.sep_entry.grid(column=3, row=2, sticky='ew')

        # Type of enumeration/Base, combobox
        ttk.Label(self.lf, text="Type").grid(column=0, row=3, sticky='w')
        self.type_base_combo = ttk.Combobox(
                                            self.lf,
                                            width=5,
                                            state='readonly',
                                            textvariable=self.type_base
                                            )
        self.type_base_combo.grid(column=1, row=3, columnspan=3, sticky='ew')
        self.type_base_combo['value'] = (
                                            'Base 10', 'Base 2', 'Base 8',
                                            'Base 16', 'Upper Case Letters',
                                            'Lower Case Letters'
                                            )
        self.type_base_combo.current(0)

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=20, row=20, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def modeGet(self, *args, **kwargs):
        return self.mode.get()

    def atNGet(self, *args, **kwargs):
        return self.at_n.get()

    def startNumGet(self, *args, **kwargs):
        return self.start_num.get()

    def incrNumGet(self, *args, **kwargs):
        return self.incr_num.get()

    def padGet(self, *args, **kwargs):
        return self.pad.get()

    def sepGet(self, *args, **kwargs):
        return self.sep.get()

    def typeBaseGet(self, *args, **kwargs):
        return self.type_base.get()

    def bindEntries(self, *args, **kwargs):
        ''' What to execute when the bindings happen. '''
        # defocus the hightlight when changing combobox
        self.mode_combo.bind('<<ComboboxSelected>>', self.defocus)
        self.type_base_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.mode.trace_add('write', fn_treeview.showNewName)
        self.at_n.trace_add('write', fn_treeview.showNewName)
        self.start_num.trace_add('write', fn_treeview.showNewName)
        self.incr_num.trace_add('write', fn_treeview.showNewName)
        self.pad.trace_add('write', fn_treeview.showNewName)
        self.sep.trace_add('write', fn_treeview.showNewName)
        self.type_base.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        '''
        self.mode_combo.selection_clear()
        self.type_base_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget. '''
        self.mode.set('None')
        self.at_n.set(0)
        self.start_num.set(0)
        self.incr_num.set(1)
        self.pad.set(1)
        self.sep.set('')
        self.type_base.set('Base 10')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.mode.set(var_dict['numbering_mode'])
        self.at_n.set(var_dict['numbering_at_n'])
        self.start_num.set(var_dict['numbering_start_num'])
        self.incr_num.set(var_dict['numbering_incr_num'])
        self.pad.set(var_dict['numbering_pad'])
        self.sep.set(var_dict['numbering_sep'])
        self.type_base.set(var_dict['numbering_type_base'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['numbering_mode'] = nb.numbering.modeGet()
        dict_['numbering_at_n'] = nb.numbering.atNGet()
        dict_['numbering_start_num'] = nb.numbering.startNumGet()
        dict_['numbering_incr_num'] = nb.numbering.incrNumGet()
        dict_['numbering_pad'] = nb.numbering.padGet()
        dict_['numbering_sep'] = nb.numbering.sepGet()
        dict_['numbering_type_base'] = nb.numbering.typeBaseGet()

    @staticmethod
    def Numbering_Rename(name, idx, *args, **kwargs):
        ''' Calls to create the numbering and then sets it up inplace '''
        mode = nb.numbering.modeGet()
        at_n = nb.numbering.atNGet()
        start_num = nb.numbering.startNumGet()
        incr_num = nb.numbering.incrNumGet()
        sep = nb.numbering.sepGet()

        # Calculate what number we are in taking into account the step and
        # the starting number
        n = idx + start_num + (incr_num - 1) * idx
        # change the number to string and whatever base we selected
        n = Numbering.Numbering_Create(n)

        if mode == 'Prefix':
            name = n + sep + name
        elif mode == 'Suffix':
            name = name + sep + n
        elif mode == 'Both':
            name = n + sep + name + sep + n
        elif mode == 'Position':
            name = name[:at_n] + sep + n + sep + name[at_n:]

        return name

    @staticmethod
    def Numbering_Create(n, *args, **kwargs):
        '''
            Changes the number to the the chosen base, removes the part of the
            string that specifies that its a number in such a base and then
            adds the padding 0s.
            For the letter cases transforms the number to what letter it would
            correspond and adds the padding As
        '''
        type_base = nb.numbering.typeBaseGet()
        pad = nb.numbering.padGet()

        # number cases
        if type_base == 'Base 10':
            n = str(n)
            n = n.rjust(pad, '0')
        elif type_base == 'Base 2':
            n = bin(n)
            n = n[2:]
            n = n.rjust(pad, '0')
        elif type_base == 'Base 8':
            n = oct(n)
            n = n[2:]
            n = n.rjust(pad, '0')
        elif type_base == 'Base 16':
            n = hex(n)
            n = n[2:]
            n = n.rjust(pad, '0')

        # letter cases
        else:
            # uses a cycle variable to know how many times it has to loop
            # ex: 1 -> A, 27 -> AA, 53 -> BA
            cycle = n // 26
            letter_n = ''
            for a in range(0, cycle + 1):
                letter_n = letter_n + string.ascii_lowercase[n - 26 * cycle]
            n = letter_n.rjust(pad, 'a')

            if type_base == 'Upper Case Letters':
                n = n.upper()

        return n


class Extension_Rep:    # (10)
    '''
        Draws the extension replacer widget. Inside rename notebook.
        10th thing to change.
        It has:
            - Dropdown to choose how to change the extension
                - Same
                - Lower case
                - Upper case
                - Title
                - Extra: adds a new extension at the end
                - Fixed: changes the extension to a new one
                - Remove
            - Entry to write the new extension for the "Extra" and the "Fixed"
            options
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Extension (10)')
        self.lf.grid(column=5, row=2, sticky='nsew')

        # Variable defs
        self.change_ext = tk.StringVar()
        self.fixed_ext = tk.StringVar()

        # Change Extension, combobox
        self.change_ext_combo = ttk.Combobox(
                                                self.lf,
                                                width=10,
                                                state='readonly',
                                                values=('Same', 'Lower',
                                                        'Upper', 'Title',
                                                        'Extra', 'Fixed',
                                                        'Remove'),
                                                textvariable=self.change_ext
                                                )
        self.change_ext_combo.grid(column=0, row=0, sticky='ew')
        self.change_ext_combo.current(0)

        # Replace extension with, entry
        self.fixed_ext_entry = ttk.Entry(
                                            self.lf,
                                            width=10,
                                            textvariable=self.fixed_ext
                                            )
        self.fixed_ext_entry.grid(column=1, row=0, sticky='ew')

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=2, row=2, sticky='w', padx=2, pady=2)

        self.bindEntries()

    def changeExtGet(self, *args, **kwargs):
        return self.change_ext.get()

    def fixedExtGet(self, *args, **kwargs):
        return self.fixed_ext.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.change_ext_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.change_ext.trace_add('write', fn_treeview.showNewName)
        self.fixed_ext.trace_add('write', fn_treeview.showNewName)

    def defocus(self, *args, **kwargs):
        '''
        Clears the highlightning of the comboboxes inside this frame
        whenever any of their changes value.
        '''
        self.change_ext_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.change_ext.set('Same')
        self.fixed_ext.set('')

    def setCommand(self, var_dict, *args, **kwargs):
        '''
            Sets the variable fields according to the loaded
            command dictionary
        '''
        self.change_ext.set(var_dict['extension_rep_change_ext'])
        self.fixed_ext.set(var_dict['extension_rep_fixed_ext'])

    @staticmethod
    def appendVarValToDict(dict_={}, *args, **kwargs):
        dict_['extension_rep_change_ext'] = nb.extension_rep.changeExtGet()
        dict_['extension_rep_fixed_ext'] = nb.extension_rep.fixedExtGet()

    @staticmethod
    def Extension_Rename(ext, *args, **kwargs):
        change_ext = nb.extension_rep.changeExtGet()
        fixed_ext = nb.extension_rep.fixedExtGet()

        if change_ext == 'Lower':
            ext = ext.lower()
        elif change_ext == 'Upper':
            ext = ext.upper()
        elif change_ext == 'Title':
            ext = ext.title()
        elif change_ext == 'Extra':
            ext = ext + '.' + fixed_ext
        elif change_ext == 'Fixed':
            ext = '.' + fixed_ext
        elif change_ext == 'Remove':
            ext = ''

        return ext


class Filters_Widget:
    '''
        Draws the filter widget. Inside rename notebook.
        It has:
            - A regular expression mask entry
            - A extension list entry
            - A folders checkbutton
            - A files checkbutton
            - A Files before Directories checkbutton
            - A hidden files checkbutton
            - A minimum name length spinbox
            - A maximum name lenght spinbox
            - A recursive depth level spinbox
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Filter File View')
        self.lf.grid(column=0, row=0, sticky='w')

        # Variable defs
        self.mask = tk.StringVar()
        self.ext = tk.StringVar()
        self.folders = tk.BooleanVar(value=True)
        self.files = tk.BooleanVar(value=True)
        self.hidden = tk.BooleanVar(value=False)
        self.files_before_dirs = tk.BooleanVar(value=False)
        self.reverse = tk.BooleanVar(value=False)
        self.min_len = tk.IntVar(value=0)
        self.max_len = tk.IntVar(value=MAX_NAME_LEN)
        self.depth = tk.IntVar(value=0)

        # Regular expression mask, entry
        ttk.Label(self.lf, text="Mask").grid(column=0, row=0, sticky='e')
        self.mask_entry = ttk.Entry(
                                    self.lf,
                                    width=10,
                                    textvariable=self.mask
                                    )
        self.mask_entry.grid(column=1, row=0, sticky='w')

        # Extension list, entry
        ttk.Label(self.lf, text="Ext(s)").grid(column=0, row=1, sticky='e')
        self.ext_entry = ttk.Entry(
                                    self.lf,
                                    width=10,
                                    textvariable=self.ext
                                    )
        self.ext_entry.grid(column=1, row=1, sticky='w')

        # Folders, checkbutton
        self.folders_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Folders',
                                                variable=self.folders,
                                                )
        self.folders_check.grid(column=2, row=0, sticky='w')

        # Files, checkbutton
        self.files_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Files',
                                                variable=self.files,
                                                )
        self.files_check.grid(column=2, row=1, sticky='w')

        # Hidden files, checkbutton
        self.hidden_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Hidden',
                                                variable=self.hidden,
                                                )
        self.hidden_check.grid(column=3, row=0, sticky='w')

        # Reverse files, checkbutton
        self.reverse_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Reverse',
                                                variable=self.reverse,
                                                )
        self.reverse_check.grid(column=3, row=1, sticky='w')

        # Files before directories, checkbutton
        self.files_before_dirs_check = ttk.Checkbutton(
                                                self.lf,
                                                text='Files before Dirs',
                                                variable=self.files_before_dirs,
                                                )
        self.files_before_dirs_check.grid(column=4, row=1, columnspan=2, sticky='w')

        # Recursive depth levels, spinbox
        ttk.Label(self.lf, text='Recursive Levels').grid(column=4, row=0, sticky='ew')
        self.depth_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    from_=-1,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.depth
                                    )
        self.depth_spin.grid(column=5, row=0)

        # Name lenght group
        ttk.Label(self.lf, text='Name lenght').grid(column=6, row=0, columnspan=4)

        # Minimum name lenght, spinbox
        ttk.Label(self.lf, text='min').grid(column=6, row=1, sticky='e')
        self.name_len_min_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.min_len
                                    )
        self.name_len_min_spin.grid(column=7, row=1, sticky='w')

        # Maximum name lenght, spinbox
        ttk.Label(self.lf, text='max').grid(column=8, row=1, sticky='e')
        self.name_len_max_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=MAX_NAME_LEN,
                                    textvariable=self.max_len
                                    )
        self.name_len_max_spin.grid(column=9, row=1, sticky='w')

        # Reset, button
        self.reset_button = ttk.Button(
                                        self.lf,
                                        width=2,
                                        text="R",
                                        command=self.resetWidget
                                        )
        self.reset_button.grid(column=10, row=1, sticky='nw', padx=2, pady=2)

        self.bindEntries()

    def maskGet(self, *args, **kwargs):
        return self.mask.get()

    def extGet(self, *args, **kwargs):
        return self.ext.get()

    def foldersGet(self, *args, **kwargs):
        return self.folders.get()

    def filesGet(self, *args, **kwargs):
        return self.files.get()

    def hiddenGet(self, *args, **kwargs):
        return self.hidden.get()

    def filesBeforeDirsGet(self, *args, **kwargs):
        return self.files_before_dirs.get()

    def reverseGet(self, *args, **kwargs):
        return self.reverse.get()

    def nameLenMinGet(self, *args, **kwargs):
        return self.min_len.get()

    def nameLenMaxGet(self, *args, **kwargs):
        return self.max_len.get()

    def depthGet(self, *args, **kwargs):
        return self.depth.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.mask_entry.bind('<FocusOut>', fn_treeview.refreshView)
        self.mask_entry.bind('<Return>', fn_treeview.refreshView)
        self.ext_entry.bind('<FocusOut>', fn_treeview.refreshView)
        self.ext_entry.bind('<Return>', fn_treeview.refreshView)
        self.folders.trace_add('write', fn_treeview.refreshView)
        self.files.trace_add('write', fn_treeview.refreshView)
        self.hidden.trace_add('write', fn_treeview.refreshView)
        self.hidden.trace_add('write', folder_treeview.refreshView)
        self.files_before_dirs.trace_add('write', fn_treeview.refreshView)
        self.reverse.trace_add('write', fn_treeview.refreshView)
        self.min_len.trace_add('write', fn_treeview.refreshView)
        self.max_len.trace_add('write', fn_treeview.refreshView)
        self.depth.trace_add('write', fn_treeview.refreshView)

    def resetWidget(self, *args, **kwargs):
        self.mask.set('')
        self.ext.set('')
        self.folders.set(True)
        self.files.set(True)
        self.hidden.set(False)
        self.files_before_dirs.set(False)
        self.reverse.set(False)
        self.min_len.set(0)
        self.max_len.set(MAX_NAME_LEN)
        self.depth.set(0)


class Rename:
    '''
        Draws the Rename button. Inside rename notebook. This is always last.
        It has:
            - Button that calls to permanently rename the selected files
            - Button that resets all fields inside the rename notebook
            - Button that reverts the last renaming action
    '''
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        # self.frame.grid(column=1, row=0, columnspan=5, sticky='w'+'e')
        self.frame.grid(column=1, row=0, sticky='w'+'e')
        # self.frame.columnconfigure(0, weight=1)

        self.load_command_button = ttk.Button(
                                        self.frame,
                                        text="Command",
                                        command=self.Apply_Command
                                        )
        self.load_command_button.grid(column=0, row=1, padx=1, pady=1, sticky='e')
        # Disable the button if no path to where commands are stored
        if not CONFIG_FOLDER_PATH:
            self.load_command_button.config(state='disable')

        self.reset_button = ttk.Button(
                                        self.frame,
                                        text="Reset",
                                        command=self.Full_Reset
                                        )
        self.reset_button.grid(column=1, row=0, padx=1, pady=1, sticky='e')

        self.revert_button = ttk.Button(
                                        self.frame,
                                        text="Undo",
                                        command=self.Undo
                                        )
        self.revert_button.grid(column=1, row=1, padx=1, pady=1, sticky='e')

        self.rename_button = ttk.Button(
                                        self.frame,
                                        text="Rename",
                                        command=self.Final_Rename
                                        )
        self.rename_button.grid(column=2, row=0, rowspan=2,
                                padx=1, pady=1, sticky='nse'
                                )

    @staticmethod
    def Full_Reset(*args, **kwargs):
        ''' Calls all resetWidget Methods '''
        nb.rename_from_file.resetWidget()
        nb.reg_exp.resetWidget()
        nb.name_basic.resetWidget()
        nb.replace.resetWidget()
        nb.case.resetWidget()
        nb.remove.resetWidget()
        nb.move_copy_parts.resetWidget()
        nb.add_to_string.resetWidget()
        nb.append_folder_name.resetWidget()
        nb.numbering.resetWidget()
        nb.extension_rep.resetWidget()

        inf_bar.lastActionRefresh('Full Reset')

    @staticmethod
    def Apply_Command(command_name=None, *args, **kwargs):
        '''
            Directly applies a command or a chain of commands.
        '''
        # Clear the last_rename list
        last_rename.clear()
        # Save what the variable fields are right now
        var_val_dict_in_use = Create_Var_Val_Dict()

        # Gets the selected command if a command_name wasn't provided
        if not command_name:
            command_name = menu_bar.selectedCommandGet()

        # Apply only if the selected command isn't the default (no changes)
        if command_name != 'DEFAULT':
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
            next_step = var_val_dict['next_step']
            if next_step:
                # Select the items that were previously selected based on the
                # last_rename list to get what are the new names
                fn_treeview.selectionSet(last_rename.newNameListGet())
                # Call Apply_Command with next_step
                Rename.Apply_Command(command_name=next_step)

            # Show that it finished
            inf_msg = 'Applied "{}" Command'.format(command_name)
            Finish_Show_Working(inf_msg=inf_msg)

        # If the selected command was the default show msg
        else:
            inf_bar.lastActionRefresh('No Command Selected')

        # Set the variable fields back to what you had prior to the command
        Set_Command_Call(var_val_dict_in_use)

    @staticmethod
    def Undo(*args, **kwargs):
        '''
            Undo the last name changes.
            You can only undo 1 step back.
        '''
        # Get a copy of the last changes list so when it gets modified it
        # doesnt affect this one and gets stuck in an infinite loop changing
        # back and forth
        # Undo the changes starting with the last one and going up
        last_rename_list = reversed(last_rename.lastRenameListGet())

        # Try to undo the changes only if there are changes to undo
        if last_rename_list:
            # Show that it's in the process
            Show_Working()

            print('Undo:')
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

            Finish_Show_Working(inf_msg='Finished Undo Operation')

            # Clear the last rename list pairs
            last_rename.clear()

        # Else show msg
        else:
            inf_bar.lastActionRefresh('No Changes to Undo')

    @staticmethod
    def Final_Rename(*args, **kwargs):
        ''' Change the selected items names according to the entry fields '''
        # Clear the last_rename action list
        last_rename.clear()
        # Get selected items
        sel_paths = list(fn_treeview.selectedItems())

        # When to reverse the naming items list so as to skip naming problems
        # like with recursiveness naming a folder before the files in it so
        # then the files can't be renamed because the path pointer doen't
        # exists. Optimized the boolean function
        # A=menu_bar.renameBotTopGet()
        # B=nb.filters.depthGet()
        # C=nb.filters.reverseGet()
        # F(A,B,C)=~BA+B~C
        if ((not nb.filters.depthGet() and menu_bar.renameBotTopGet()) or
            (nb.filters.depthGet() and not nb.filters.reverseGet())):
            sel_paths = reversed(sel_paths)

        # Try to apply the changes only if there is a selection
        if sel_paths:
            # Show that its in the process
            Show_Working()

            print('Rename:')
            for path in sel_paths:
                path_tuple = path.rpartition('/')
                name = fn_treeview.tree_folder.set(path, '#1')
                new_path = path_tuple[0] + path_tuple[1] + name

                System_Rename(path, new_path)
            print()

            Refresh_Treeviews()

            # Show that its finish
            Finish_Show_Working(inf_msg='Finished Rename')

        # Else show a msg that there is no selection
        else:
            inf_bar.lastActionRefresh('No Selected Items')


###################################
'''
METADATA CLASSES
'''
###################################


class Metadata_ListEntries:
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=0, row=0, sticky='nsw')

        self.frame.grid(sticky='n'+'s')
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.field_frame = VerticalScrolledFrame(self.frame)
        self.field_frame.grid(
                                column=0, row=0, columnspan=3,
                                pady=3, sticky='nsw'
                                )

        self.new_tag_name = tk.StringVar()

        ttk.Label(self.frame, text='New Tag Name').grid(
                                                        column=0,
                                                        row=1,
                                                        )
        self.new_tag_name_entry = ttk.Entry(
                                            self.frame,
                                            textvariable=self.new_tag_name,
                                            )
        self.new_tag_name_entry.grid(column=1, row=1, sticky='w'+'e')

        # Add new tag, button
        self.add_field_button = ttk.Button(
                                            self.frame,
                                            width=5,
                                            text="Add",
                                            command=self.createMetadataTag
                                            )
        self.add_field_button.grid(column=2, row=1, sticky='se')

        self.metaDictReset()

        self.metadataEntriesCreate()

    def newTagNameGet(self, *args, **kwargs):
        return self.new_tag_name.get()

    def metaDictTextGet(self, key, *args, **kwargs):
        return self.meta_dict[key].get()

    def metaDictGet(self, *args, **kwargs):
        return self.meta_dict

    def metaDictReset(self, *args, **kwargs):
        self.meta_dict = {'title': tk.StringVar(),
                            'tracknumber': tk.StringVar(),
                            'artist': tk.StringVar(), 'album': tk.StringVar(),
                            'date': tk.StringVar(), 'genre': tk.StringVar()}

    def getMetadata(self, selection, *args, **kwargs):
        '''
        Create a dictionary that has all the same keys than the metadata
        and the values are all the values together of all selected items.
        Then removes duplicate values
        Ex:
            Item1 = {1:'a', 2:'b'}
            Item2 = {1:'a', 2:'c', 3:'d'}

            Result = {1:['a'], 2:['b', 'c'], 3:'d'}

        Finally it transforms each value key to a tkinter.tk.StringVar()
        with a default value thats the list transformed into a string with
        each item separated by "; ".
        Error handling for when the selected items don't have metadata.
        '''
        self.meta_dict = {'title': [], 'tracknumber': [], 'artist': [],
                            'album': [], 'date': [], 'genre': []}
        try:
            for file in selection:
                meta_audio = Meta_Audio(file)

                for meta_item in meta_audio:
                    meta_value = meta_audio.get(meta_item)

                    # Adds to each key the value for this selected item
                    self.meta_dict[meta_item] = (
                                        self.meta_dict.get(meta_item, list()) +
                                        meta_value
                                        )

            for key in self.meta_dict:
                # Remove duplicates
                self.meta_dict[key] = No_Duplicate_List(self.meta_dict[key])
                # List to string
                str_value = self.metaValuesListToStr(self.meta_dict[key])

                # Set each key value to a StringVar
                self.meta_dict[key] = tk.StringVar(value=str_value)

            return self.meta_dict

        except TypeError:
            print('Not a Valid Audio File')
            self.metaDictReset()
            return self.meta_dict

    def metaValuesListToStr(self, list_convert, *args, **kwargs):
        '''
            Transforms a list into a string separating each value with "; "
        '''
        return '; '.join(list_convert)

    def entryFrameReset(self, *args, **kwargs):
        '''
            Reset the entry list by deleting all widgets inside
            the entry widget
        '''
        for child in self.field_frame.interior.winfo_children():
            child.destroy()

    def metadataSelect(self, *args, **kwargs):
        '''
            Resets the frame and repopulates with all the entries and
            their corresponding labels
        '''
        selection = fn_treeview.selectedItems()
        self.entryFrameReset()
        self.getMetadata(selection)
        self.metadataEntriesCreate()

    def metadataEntriesCreate(self, *args, **kwargs):
        ''' Create the metadata list entries with their values'''
        for n, key in enumerate(self.meta_dict):
            ttk.Label(
                        self.field_frame.interior,
                        text=key, width=25, anchor='e'
                        ).grid(column=0, row=n)

            ttk.Entry(
                        self.field_frame.interior,
                        width=55,
                        textvariable=self.meta_dict[key]
                        ).grid(column=1, row=n, sticky='e')

    def createMetadataTag(self, *args, **kwargs):
        '''
            Adds a new tag to the metadata tags entries list if the tag
            name is not empty.
        '''
        tag_name = self.newTagNameGet()

        if tag_name:
            self.meta_dict[tag_name] = tk.StringVar()
            n = len(self.meta_dict)

            ttk.Label(
                        self.field_frame.interior,
                        text=tag_name, width=25, anchor='e'
                        ).grid(column=0, row=n)
            ttk.Entry(
                        self.field_frame.interior,
                        width=55,
                        textvariable=self.meta_dict[tag_name]
                        ).grid(column=1, row=n, sticky='e')

        else:
            msg = 'No name for the new tag. Please type a name'
            inf_bar.lastActionRefresh(msg)


class Metadata_Img:
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=1, row=0, sticky='ns')

        # Empty photo image to force the label to use pixel size
        self.photo_image = tk.PhotoImage()

        self.picture = None
        self.image_path = tk.StringVar()

        # Path to new image, entry
        self.image_path_entry = ttk.Entry(
                                            self.frame,
                                            textvariable=self.image_path
                                            )
        self.image_path_entry.grid(column=0, row=0, sticky='ew')

        self.reset_path_button = ttk.Button(
                                            self.frame,
                                            width=2,
                                            text="X",
                                            command=self.resetPath
                                            )
        self.reset_path_button.grid(column=1, row=0, sticky='w')

        # Image frame, Label
        self.img = tk.Label(
                            self.frame,
                            relief='sunken',
                            background='gray10',
                            image=self.photo_image,
                            height=250,
                            width=250
                            )
        self.img.grid(column=0, row=1)

        # Image size, label
        self.size_label = ttk.Label(self.frame, text='No Image')
        self.size_label.grid(column=0, row=2)

    def imageGet(self, *args, **kwargs):
        return self.picture

    def imagePathGet(self, *args, **kwargs):
        return self.image_path.get()

    def resetPath(self, *args, **kwargs):
        self.image_path.set('')

    def imageLoad(self, *args, **kwargs):
        '''
            Loads the first image binded to the selected files and checks if
            they are all the same. If not then it loads no image.
            Also does nothing if the file doesnt have an image attached.
        '''
        # Error handling if theres no image
        try:
            selection = fn_treeview.selectedItems()
            file = selection[0]
            self.picture = Meta_Picture(file)

            for file in selection:
                img_comparison = Meta_Picture(file)

                # Checks against that first loaded image every other
                # image in the selection. Becomes true when any of the other
                # images are different
                if img_comparison != self.picture:
                    self.picture = None
                    self.size_label.config(text='Different images')

                    break

        except (IndexError, AttributeError):
            # Set the size label to show theres no image
            self.size_label.config(text='No image')

    def imageShow(self, *args, **kwargs):
        ''' Shows the first image binded to the files '''
        self.picture = None
        self.imageLoad()
        if self.picture is not None:
            im = PIL.Image.open(BytesIO(self.picture))
            # Get image size before resizing
            im_width, im_height = map(str, im.size)

            # Resize
            im = im.resize((250, 250), PIL.Image.ANTIALIAS)

            # Show image
            render = PIL.ImageTk.PhotoImage(im)
            self.img.image = render
            self.img.config(image=render)

            # Show image size
            size_text = '{} x {}'.format(im_width, im_height)
            self.size_label.config(text=size_text)

        else:
            self.img.config(image=self.photo_image)
            self.size_label.config(text='No Image/Different Images')


class Apply_Changes:
    '''
        Apply chnages widget. Inside the metadata notebook.
        It has:
            - Button to apply the metadata changes
            - Button to apply the image changes
            - Button to apply both
    '''
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=2, row=0, sticky='se')

        self.apply_meta_button = ttk.Button(
                                    self.frame,
                                    width=10,
                                    text="Apply Meta",
                                    command=self.metaChangesCall
                                    )
        self.apply_meta_button.grid(column=0, row=0, sticky='e')

        self.apply_img_button = ttk.Button(
                                    self.frame,
                                    width=10,
                                    text="Apply Img",
                                    command=self.imgChangesCall
                                    )
        self.apply_img_button.grid(column=0, row=1, sticky='e')

        self.apply_all_button = ttk.Button(
                                    self.frame,
                                    width=10,
                                    text="Apply All",
                                    command=self.allChangesCall
                                    )
        self.apply_all_button.grid(column=0, row=2, sticky='e')

    def metaChangesCall(self, *args, **kwargs):
        '''
            Calls the procedure to only change metadata tags.
            Loads the new values from the list of entries and sets them up.
        '''
        selection = fn_treeview.selectedItems()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Show that its in the process
        Show_Working()

        for item in selection:
            meta_audio = Meta_Audio(item)
            for key in meta_dict:
                value = nb.metadata_list_entries.metaDictTextGet(key)

                self.applyMetaChanges(meta_audio, key, value)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg='Metadata Changed')

    def applyMetaChanges(self, meta_audio, key, value, *args, **kwargs):
        '''
            Applies the changes to the metadata. Skips the instances where
            there are several values (so as not to set all values to every
            item) and removes empty tags (if they also exist in the metadata
            tags of the item).
        '''
        # If there is more than one value for the field, skip it
        if ';' not in value:
            if value:
                # Tags can have any name in vorbis comment (flac metadata) but
                # not in ID3 (mp3 metadata), so if you try adding a tag with a
                # name thats not accepted in ID3 it'll raise and error
                try:
                    meta_audio[key] = value
                except (EasyID3KeyError, EasyMP4KeyError):
                    msg = 'Undefined Tag name "{}" for ID3/MP4. Skipped'.format(key)
                    Error_Frame(msg)

            # Delete empty values only when they exist in the metadata
            # of the file
            elif not value and key in meta_audio:
                meta_audio.pop(key)

        meta_audio.save()

    def imgChangesCall(self, *args, **kwargs):
        '''
            Calls the procedure to only change the image metadata.
            Loads the new image and then iterates over each item setting
            the picture.
        '''
        selection = fn_treeview.selectedItems()
        img_path = nb.metadata_img.imagePathGet()

        # Show that its in the process
        Show_Working()

        if img_path.endswith(('.jpg', '.jpeg', '.png')) and os.path.exists(img_path):
            # Load the new image
            img, apic = self.loadImage(img_path)
            for item in selection:
                # Load the item metadata and set the new picture.
                if item.endswith('.flac'):
                    meta_audio = FLAC(item)
                    self.applyImgChangesFLAC(meta_audio, img)
                elif item.endswith('.mp3'):
                    meta_audio = ID3(item)
                    self.applyImgChangesMP3(meta_audio, apic)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg='Image Changed')

    def loadImage(self, img_path, *args, **kwargs):
        '''
            Creates a mutagen.flac.Picture object, sets its mimetype, its
            type and its description. Then loads the selected img and returns
            the Picture object.
        '''
        # Set the corresponding mime type
        if img_path.endswith('.png'):
            mime_type = 'image/png'
        else:
            mime_type = 'image/jpg'

        # Open bytes like object for the image
        albumart = open(img_path, 'rb').read()

        # create img object for flacs and set its properties
        img = FlacPicture()
        # type 3 is for cover image
        img.type = 3
        # Set the corresponding mime type
        img.mime = mime_type
        # Set description
        img.desc = 'front cover'
        img.data = albumart

        # Create Image object for mp3s and set its properties
        apic = APIC(
                    encoding=3,
                    mime=mime_type,
                    type=3, desc='front cover',
                    data=albumart
                    )

        return img, apic

    def applyImgChangesFLAC(self, meta_audio, img=None, *args, **kwargs):
        ''' Changes the image of a flac audio file '''
        if img:
            meta_audio.clear_pictures()     # clear other images
            meta_audio.add_picture(img)     # set new image
            meta_audio.save()

    def applyImgChangesMP3(self, meta_audio, apic=None, *args, **kwargs):
        ''' Changes the image of a mp3 audio file '''
        if apic:
            for tag in meta_audio:
                if 'APIC' in tag:
                    meta_audio.delall(tag)
                    break
            meta_audio['APIC'] = apic

            meta_audio.save()

    def allChangesCall(self, *args, **kwargs):
        ''' Calls to both the metadata change and the image change '''
        selection = fn_treeview.selectedItems()
        img_path = nb.metadata_img.imagePathGet()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Show that its in the process
        Show_Working()

        if img_path.endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
            img, apic = self.loadImage(img_path)
        else:
            img = apic = None

        for item in selection:
            # Change the image
            if item.endswith('flac'):
                meta_audio = FLAC(item)
                self.applyImgChangesFLAC(meta_audio, img)
            elif item.endswith('mp3'):
                meta_audio = ID3(item)
                self.applyImgChangesMP3(meta_audio, apic)

            # Load the metadata for flacs and easyid3 for mp3s
            meta_audio = Meta_Audio(item)
            # Change the metadata tags
            for key in meta_dict:
                value = nb.metadata_list_entries.metaDictTextGet(key)

                self.applyMetaChanges(meta_audio, key, value)

        # Reload after the changes
        Populate_Fields()
        # Show that its finish
        Finish_Show_Working(inf_msg='Metadata and Image Changed')


def Meta_Audio(file, *args, **kwargs):
    ''' Returns the metadata from the audio file '''
    if file.endswith('.flac'):
        meta_audio = FLAC(file)
    elif file.endswith('.mp3'):
        meta_audio = MP3(file, ID3=EasyID3)
    elif file.endswith('.mp4'):
        meta_audio = EasyMP4(file)
    else:
        meta_audio = None

    return meta_audio


def Meta_Picture(file, *args, **kwargs):
    '''
        Gets the attached picture from the metadata, if there is one, if not
        returns None.
    '''
    meta_picture = None
    if file.endswith('flac'):
        meta_picture = FLAC(file).pictures[0].data
    elif file.endswith('mp3'):
        meta_audio = ID3(file)
        # Because the attached picture in mp3 files can have many names
        # and the only common factor is having APIC in the key, check all keys
        # and see if theres any that contains APIC
        for tag in meta_audio:
            if 'APIC' in tag:
                meta_picture = meta_audio.get(tag).data
                break

    return meta_picture


def Title_Track_From_File(*args, **kwargs):
    '''
        Sets the title and tracknumber metadata getting its values from the
        filename. It splits the filename at the first apparition of "-" and
        sets the left part to be the tracknumber and the right part to be
        the title.
    '''
    Show_Working()

    selection = fn_treeview.selectedItems()

    for item in selection:
        # Get the metadata
        meta_audio = Meta_Audio(item)
        # Get the filename
        name = fn_treeview.oldNameGet(item)

        # Split filename
        n, title = name.split('-', 1)
        # Remove the extension from the title
        title, ext = De_Ext(title)

        # Set the new metadata values
        meta_audio['title'] = title.strip()
        meta_audio['tracknumber'] = n.strip()

        meta_audio.save()

    Populate_Fields()
    msg = 'Changed "title" and "tracknumber" according to filename'
    Finish_Show_Working(inf_msg=msg)


def Format_Track_Num_Meta(*args, **kwargs):
    ''' Format metadata's tracknumber to be a single 2 digits number '''
    Show_Working()

    selection = fn_treeview.selectedItems()

    for item in selection:
        # Get the metadata
        meta_audio = Meta_Audio(item)
        # Specifically the tracknumber (which is a list so get the first item)
        n = meta_audio['tracknumber'][0]

        # Remove everything after "/" (inclusive)
        n = n.partition('/')[0]
        # Add left padding of 0s
        n = n.rjust(2, '0')

        # Set the tracknumber
        meta_audio['tracknumber'] = n
        meta_audio.save()

    Populate_Fields()
    Finish_Show_Working(inf_msg='Changed "tracknumber" format')


###################################
'''
CONFIG, LOGS & COMMAND FILES
'''
###################################


class Save_Command_Name_Window:
    def __init__(self, *args, **kwargs):
        self.frame = tk.Toplevel(root, bg='gray85')
        self.frame.title('Choose Name for Command')
        self.frame.attributes('-type', 'dialog')

        # Variable defs
        self.command_name = tk.StringVar()
        self.prev_step = tk.StringVar()

        # Extended Replace, entry
        txt = 'Choose a Name for The New Command (only letters)'
        ttk.Label(self.frame, text=txt).grid(column=0, row=0, columnspan=2, sticky='w')
        self.name_entry = ttk.Entry(
                                    self.frame,
                                    textvariable=self.command_name
                                    )
        self.name_entry.grid(column=0, row=1, columnspan=2, sticky='ew')
        self.name_entry.focus()

        # Previous Step, combobox
        steps_list = COMMAND_CONF.sections()
        steps_list.insert(0, 'None')
        txt = 'Select Previous Step'
        ttk.Label(self.frame, text=txt).grid(column=0, row=2, sticky='w')
        self.steps_combo = ttk.Combobox(
                                        self.frame,
                                        width=10,
                                        state='readonly',
                                        values=steps_list,
                                        textvariable=self.prev_step
                                        )
        self.steps_combo.grid(column=1, row=2, sticky='ew')
        self.steps_combo.current(0)

        # Cancel, button
        self.cancel_button = ttk.Button(
                                        self.frame,
                                        text="Cancel",
                                        command=self.frame.destroy
                                        )
        self.cancel_button.grid(column=0, row=3)

        # Save and exit Window, Button
        self.save_button = ttk.Button(
                                        self.frame,
                                        text="Save",
                                        command=self.saveExit
                                        )
        self.save_button.grid(column=1, row=3)

        self.bindEntries()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.steps_combo.bind('<<ComboboxSelected>>', self.defocus)

    def defocus(self, *args, **kwargs):
        '''
        Clears the highlightning of the comboboxes inside this frame
        whenever any of them changes value.
        '''
        self.steps_combo.selection_clear()

    def commandNameGet(self, *args, **kwargs):
        return self.command_name.get()

    def prevStepGet(self, *args, **kwargs):
        prev_step = self.prev_step.get()
        if prev_step != 'None':
            return prev_step
        else:
            return ''

    def saveExit(self, *args, **kwargs):
        command_name = self.commandNameGet()
        prev_step = self.prevStepGet()

        if not command_name.isalnum():
            Error_Frame('Invalid Name')
        elif command_name in COMMAND_CONF:
            Error_Frame('Name Already in Use')
        else:
            Save_To_Command_File(command_name, prev_step)
            self.frame.destroy()


def Create_Config_Folder(path, *args, **kwargs):
    ''' Creates the config folder if it doesn't exist already '''
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass


def Save_To_Command_File(command_name, prev_step='', *args, **kwargs):
    ''' Saves the current entries varibales configuration as a command '''
    # Get the current variable config
    command_dict = Create_Var_Val_Dict()

    # Added to the configparser object
    COMMAND_CONF[command_name] = command_dict
    # If a previous step was selected modify the previous step adding the
    # next_step
    if prev_step:
        COMMAND_CONF[prev_step]['next_step'] = command_name

    # Save changes
    with open(COMMAND_CONF_FILE, 'w') as conf_file:
        COMMAND_CONF.write(conf_file)

    # Update command menu list and show info msg
    menu_bar.updateCommandListMenu()
    inf_msg = 'Saved Field States as Command "{}"'.format(command_name)
    inf_bar.lastActionRefresh(inf_msg)


def Delete_Command(*args, **kwargs):
    ''' Deletes seletec command from the command configuration file '''
    # Get selected command
    command_name = menu_bar.selectedCommandGet()
    # Pop it
    COMMAND_CONF.pop(command_name)

    # Save changes
    with open(COMMAND_CONF_FILE, 'w') as conf_file:
        COMMAND_CONF.write(conf_file)

    # Update the command list in the menu and show info msg
    menu_bar.updateCommandListMenu()
    inf_msg = 'Deleted "{}" Command'.format(command_name)
    inf_bar.lastActionRefresh(inf_msg)


def Create_Var_Val_Dict(*args, **kwargs):
    '''
        Call for each widget to retrive the variable values in their fields anc
        create a dictionary with the current configuration.
    '''
    var_val_dict = {}

    Rename_From_File.appendVarValToDict(var_val_dict)
    Reg_Exp.appendVarValToDict(var_val_dict)
    Name_Basic.appendVarValToDict(var_val_dict)
    Replace.appendVarValToDict(var_val_dict)
    Case.appendVarValToDict(var_val_dict)
    Remove.appendVarValToDict(var_val_dict)
    Move_Copy_Parts.appendVarValToDict(var_val_dict)
    Add_To_String.appendVarValToDict(var_val_dict)
    Append_Folder_Name.appendVarValToDict(var_val_dict)
    Numbering.appendVarValToDict(var_val_dict)
    Extension_Rep.appendVarValToDict(var_val_dict)

    var_val_dict['next_step'] = ''

    return var_val_dict


def Load_Command_Call(*args, **kwargs):
    ''' Loads the selected command to the entries fields '''
    command_name = menu_bar.selectedCommandGet()

    # If the selected command isn't the default loads the dictionary from the
    # configuration file
    if command_name != 'DEFAULT':
        var_val_dict = dict(COMMAND_CONF.items(command_name))

        # Call to set the dictionary
        Set_Command_Call(var_val_dict)

        # Show info msg
        inf_msg = 'Loaded "{}" Fields Configuration'.format(command_name)
        inf_bar.lastActionRefresh(inf_msg)

    # Else show an error info msg
    else:
        inf_bar.lastActionRefresh('No selected Command')


def Set_Command_Call(dict_={}, *args, **kwargs):
    ''' Call each widget to set the entries values from the given dict '''
    nb.rename_from_file.setCommand(dict_)
    nb.reg_exp.setCommand(dict_)
    nb.name_basic.setCommand(dict_)
    nb.replace.setCommand(dict_)
    nb.case.setCommand(dict_)
    nb.remove.setCommand(dict_)
    nb.move_copy_parts.setCommand(dict_)
    nb.add_to_string.setCommand(dict_)
    nb.append_folder_name.setCommand(dict_)
    nb.numbering.setCommand(dict_)
    nb.extension_rep.setCommand(dict_)


###################################
'''
GENERAL FUNCTIONS
'''
###################################


def Scandir_Recursive(path, mask=re.compile(''), ext_tuple=[],
    folders=True, files=True, hidden=False, min_len=0, max_len=MAX_NAME_LEN,
    depth=0, *args, **kwargs):
    '''
        A scandir implementation that allows recursiveness by level and returns
        a list of os.DirEntry objects.
        Depth starts at the maximum value and goes down by one in each function
        call until it reaches 0 where it doesn't call the function anymore.
        If the depth is -1 execute maximum recursiveness.
    '''
    tree = []
    
    try:
        # Loop through scandir
        for entry in os.scandir(path):
            # BIIIG filter logic check to add entries
            if (mask.match(entry.name) and
                (not ext_tuple or entry.name.endswith(ext_tuple)) and
                ((folders and entry.is_dir(follow_symlinks=False)) or
                (files and entry.is_file())) and
                (hidden or not entry.name.startswith('.')) and
                (min_len <= len(entry.name) <= max_len)):

                tree.append(entry)

            # When entry.is_dir
            if (entry.is_dir(follow_symlinks=False) and
                (hidden or not entry.name.startswith('.'))):
                # If depth is already 0 skip and continue with the next step
                # of the loop
                if depth == 0:
                    continue
                # If the depth is larger than 0 call the function again
                # with depth-1. That'll produce that when it finds another
                # directory inside it it will call the function with
                # (depth-1)-1. It'll do that until there are no more folders
                # in which case it will go back up to where it left off
                # and repeat
                elif depth > 0:
                    next_depth = depth - 1
                # And if depth is -1 call the function again with depth=-1.
                # This will cause to call the function in every possible
                # folder
                elif depth == -1:
                    next_depth = -1

                # Call the function again inside the directory
                sub_tree = Scandir_Recursive(entry.path, mask=mask,
                                                ext_tuple=ext_tuple,
                                                folders=folders, files=files,
                                                hidden=hidden, min_len=min_len,
                                                max_len=max_len,
                                                depth=next_depth)

                tree = tree + sub_tree

    # Unless it catches any of this errors
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        pass

    return tree


def Tree_Sort(tree, depth=-1, files_before_dirs=False,
    reverse=False, *args, **kwargs):
    ''' Sort the tree list with a few options '''
    # When depth wasn't 0 sort alphabetically and case-insensitively (casefold)
    # the absolute paths, this will produce having a folder followed by
    # its contents
    if depth != 0:
        tree.sort(key=lambda entry: entry.path.casefold(), reverse=reverse)

    # When the depth is 0 order the list first by directories first then files
    # or viceversa depending on the files_before_dirs flag, and then by name
    # case-insensitevely (casefold)
    else:
        tree.sort(key=lambda entry:
                    (entry.is_dir() if files_before_dirs else entry.is_file(),
                    entry.name.casefold()), reverse=reverse)

    return tree


def Populate_Fields(*args, **kwargs):
    '''
        What to show and what to have active when each notebook tab is active.
    '''
    # Get active tab
    tab = nb.nbTabGet()

    if tab == 'Rename':
        # Shows new naming
        fn_treeview.resetNewName()
        fn_treeview.showNewName()
        # Enables the menu options for renaming
        menu_bar.renameEnable()
        # Disables the menu options for metadata
        menu_bar.metadataDisable()

    elif tab == 'Metadata':
        # Stops showing new name
        fn_treeview.resetNewName()
        # Enables loading metadata
        nb.metadata_list_entries.metadataSelect()
        nb.metadata_img.imageShow()
        # Enables the menu options for metadata
        menu_bar.metadataEnable()
        # Disables the menu options for renaming
        menu_bar.renameDisable()


def No_Duplicate_List(list_convert, *args, **kwargs):
    return list(dict.fromkeys(list_convert))


def Show_Working(inf_msg='Working...', *args, **kwargs):
    '''
        Sets the cursor to watch and empties the info msg to show that
        you have to wait.
        Remember calling Finish_Show_Working() after the work is done.
    '''
    # Set mouse pointer to watch
    root.config(cursor='watch')
    # Delete the last action text from the info bar
    inf_bar.lastActionRefresh(inf_msg)
    # Needs the update call so the window can apply this changes
    root.update()


def Finish_Show_Working(inf_msg='Done', *args, **kwargs):
    ''' Sets cursor to arrow and sets the info msg. '''
    # Set mouse pointer back to arrow
    root.config(cursor='arrow')
    # Show that its finish by setting the info bar message.
    inf_bar.lastActionRefresh(inf_msg)


def Call_For_Info_Bar(*args, **kwargs):
    inf_bar.numItemsRefresh()


def Refresh_Treeviews(*args, **kwargs):
    ''' Refreshes Both Treeviews '''
    # Update the file view
    fn_treeview.refreshView()
    # Update the folder view
    folder_treeview.updateNode()

    inf_bar.lastActionRefresh('Refreshed Both Treeviews')


def New_Naming(name, idx, path, *args, **kwargs):
    '''
    Creates the new name going through all fields and making the changes
    to the old_name string
    '''
    # Separate name and extension
    name, ext = De_Ext(name)

    name = Rename_From_File.Rename_From_File_Rename(name, idx)  # (0)
    name = Reg_Exp.Reg_Exp_Rename(name)                         # (1)
    name = Name_Basic.Name_Basic_Rename(name)                   # (2)
    name = Replace.Replace_Action(name)                         # (3)
    name = Case.Case_Change(name)                               # (4)
    name = Remove.Remove_Rename(name)                           # (5)
    name = Move_Copy_Parts.Move_Copy_Action(name)               # (6)
    name = Add_To_String.Add_Rename(name)                       # (7)
    name = Append_Folder_Name.Append_Folder_Rename(name, path)  # (8)
    name = Numbering.Numbering_Rename(name, idx)                # (9)

    ext = Extension_Rep.Extension_Rename(ext)                   # (10)

    # Remove leading and trailing whitespaces and re-add the extension
    name = name.strip() + ext

    # Format any metadata fields that have been added to the name
    # (only if the metadata modules were imported)
    if METADATA_IMPORT:
        name = Meta_Format(name, path)

    return name


def De_Ext(name, *args, **kwargs):
    '''
    Removes the extension from the selected path.
    Returns the name of the field and the extension separate.
    If theres no extension returns an empty extension.
    '''
    file_name, dot, ext = name.rpartition('.')
    if file_name != '':
        ext = dot + ext
        name = file_name
    else:
        ext = ''

    return name, ext


def Meta_Format(str_, path, *args, **kwargs):
    ''' Format the string with the values from the metadata dictionary '''
    # Only load the metadata if the string contains '{' and '}'
    if ('{' and '}') in str_:
        meta_audio = Meta_Audio(path)

        # If the past function returned something (it was a valid file)
        if meta_audio:
            # Get a dict that's the same as meta_audio but only the first
            # item of each key (because the metadata is a dict of lists)
            metadata = {item: meta_audio[item][0] for item in meta_audio}
            # Get a list of the keys in the dict adding the string between
            # curly braces
            field_list = ['{'+key+'}' for key in metadata.keys()]

            # Individually check and replace for each possible key in the dict
            # (need to do this because if you want to use curly braces in the
            # string i would raise an error and would skip any actual editing)
            for field in field_list:
                str_ = str_.replace(field, field.format(**metadata))

    return str_


def System_Rename(file, new_path, *args, **kwargs):
    ''' Changes the name of the files in the system '''
    if not os.path.exists(new_path):
        try:
            os.rename(file, new_path)
            last_rename.appendRenamePair(file, new_path)

            print('{} -> {}'.format(file, new_path))

        # Catch exceptions for invalid filenames
        except OSError:
            msg = "Couldn't rename file {}.\nInvalid characters".format(file)
            Error_Frame(error_desc=msg)
            inf_bar.lastActionRefresh("Couldn't Rename file. Invalid characters")

        except FileNotFoundError:
            msg = "Couldn't rename file {}.\nFile not found".format(file)
            Error_Frame(error_desc=msg)
            inf_bar.lastActionRefresh("Couldn't Rename file. File not found")

    # If path already exists don't write over it and skip it
    else:
        msg = "Couldn't rename file {}.\nPath already exists".format(file)
        Error_Frame(error_desc=msg)
        inf_bar.lastActionRefresh("Couldn't Rename file. Path already exists")


def Root_Binds(*args, **kwargs):
    ''' Key bindings for the whole program '''
    # "A" and "a" are different keys

    # Entries Reset
    root.bind('<Control-t>', Rename.Full_Reset)
    root.bind('<Control-T>', Rename.Full_Reset)
    # Rename
    root.bind('<Control-r>', Rename.Final_Rename)
    root.bind('<Control-R>', Rename.Final_Rename)
    root.bind('<Control-z>', Rename.Undo)
    root.bind('<Control-Z>', Rename.Undo)
    # Refresh
    root.bind('<F5>', fn_treeview.refreshView)
    root.bind('<Control-F5>', folder_treeview.refreshView)
    # Selection
    root.bind('<Control-a>', fn_treeview.selectAll)
    root.bind('<Control-A>', fn_treeview.selectAll)
    root.bind('<Control-d>', fn_treeview.deselectAll)
    root.bind('<Control-D>', fn_treeview.deselectAll)
    root.bind('<Control-i>', fn_treeview.invertSelection)
    root.bind('<Control-I>', fn_treeview.invertSelection)
    # Command
    root.bind('<Control-e>', Load_Command_Call)
    root.bind('<Control-E>', Load_Command_Call)


###################################
'''
PROGRAM
'''
###################################

if __name__ == '__main__':

    '''
    PROGRAM INITIALIZATION
    '''
    if CONFIG_FOLDER_PATH:
        Create_Config_Folder(CONFIG_FOLDER_PATH)
    last_rename = Last_Rename()

    '''
    WINDOW INITIALIZATION
    '''
    root = tk.Tk()
    root.title(TITLE)
    root.attributes('-type', 'dialog')  # makes the window a pop up/dialog

    '''
    MAINFRAME AND SUBFRAMES
    '''
    mainframe = ttk.Frame(root, padding='5 5 5 5')
    mainframe.grid(column=0, row=0, sticky='nwes')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Tree view & File view
    # Frame Creation for the folder treeview, file view and the directory entry
    f_t_view_frame = ttk.Frame(mainframe)
    f_t_view_frame.grid(column=0, row=0, sticky='w'+'e')
    f_t_view_frame.columnconfigure(1, weight=1)
    fn_treeview = FileNavigator(f_t_view_frame)
    folder_treeview = TreeNavigator(f_t_view_frame, path=PATH)
    dir_entry_frame = DirEntryFrame(f_t_view_frame)

    # Extra Information Bar
    inf_bar = InfoBar(mainframe)

    # Notebook
    nb = ChangesNotebook(mainframe)

    # Menubar
    menu_bar = Top_Menu(root)

    # Set Padding around the window
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Initialize the treeview
    folder_treeview.refreshView()
    # Initialize the global key bindings
    Root_Binds()

    root.config(menu=menu_bar.menubar)
    root.mainloop()
