import tkinter as tk
import webbrowser  # for the About menu
from tkinter import ttk

import batchpynamer as bpn
from batchpynamer import basewidgets, commands
from batchpynamer.notebook.metadata import metadata, utils
from batchpynamer.notebook.rename import rename


class TopMenu(tk.Menu):
    def __init__(self):
        pass

    def tk_init(self, master):
        super().__init__(master, bg="gray75", foreground="black")

        # Create the menus and add them to the main bar
        self.fileMenu()
        self.add_cascade(label="File", menu=self.file_menu)

        self.selectionMenu()
        self.add_cascade(label="Selection", menu=self.selection_menu)

        # Only create the command menu if there is a configuration folder
        self.commandMenu()
        self.add_cascade(label="Commands", menu=self.command_menu)
        if not bpn.CONFIG_FOLDER_PATH:
            self.entryconfigure(index=3, state="disable")

        self.aboutMenu()
        self.add_cascade(label="About", menu=self.about_menu)

        # self.changes_notebook.menu_bar = self

        self.metadataDisable()

    def fileMenu(self, *args, **kwargs):
        """File Menu Dropdown"""
        self.rename_bot_top = tk.BooleanVar()

        # Create the menu
        self.file_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Rename
        self.file_menu.add_command(
            label="Rename",
            command=rename.final_rename,
            accelerator="Ctrl+R",
        )

        # Undo Rename
        self.file_menu.add_command(
            label="Undo Rename",
            command=rename.undo_rename,
            accelerator="Ctrl+Z",
        )

        # Reset Entry Fields
        self.file_menu.add_command(
            label="Reset Entry Fields",
            command=rename.full_reset,
            accelerator="Ctrl+T",
        )

        # Rename from Bottom to Top
        self.file_menu.add_checkbutton(
            label="Activate renaming from Bottom to Top",
            variable=self.rename_bot_top,
        )

        # Separator
        self.file_menu.add_separator()

        # Create the metadata menu options only if the metadata modification
        # is active (the dependencies have been exported)
        if bpn.METADATA_IMPORT:
            # Apply Metadata Changes
            self.file_menu.add_command(
                label="Apply Metadata Changes",
                command=bpn.metadata_apply_changes.metaChangesCall,
            )

            # Apply Image Metadata
            self.file_menu.add_command(
                label="Apply Image Metadata Change",
                command=bpn.metadata_apply_changes.imgChangesCall,
            )

            # Apply Both Image & Metadata Changes
            self.file_menu.add_command(
                label="Apply Both Image & Metadata Changes",
                command=bpn.metadata_apply_changes.allChangesCall,
            )

            # Set the title and the tracknumber metadata from the filename
            self.file_menu.add_command(
                label='Set "title" & "tracknumber" from filename',
                command=utils.title_track_from_file,
            )

            # Format tracknumber metadata field
            self.file_menu.add_command(
                label='Format "tracknumber"',
                command=utils.format_track_num_meta,
            )

            # Separator
            self.file_menu.add_separator()

        # Refresh Files
        self.file_menu.add_command(
            label="Refresh File View",
            command=bpn.fn_treeview.refreshView,
            accelerator="F5",
        )

        # Refresh Focused Node in Tree
        self.file_menu.add_command(
            label="Refresh Focused Node",
            command=bpn.dir_entry_frame.focusFolderRefresh,
            accelerator="Ctrl+F5",
        )

        # Refresh Whole Tree
        self.file_menu.add_command(
            label="Refresh Full Directory Browser",
            command=bpn.dir_entry_frame.folderNavRefresh,
            accelerator="Ctrl+Shift+F5",
        )

        # Separator
        self.file_menu.add_separator()

        # Exit
        self.file_menu.add_command(
            label="Exit",
            command=bpn.root.quit,
            accelerator="Ctrl+Esc",
        )

    def renameBotTopGet(self, *args, **kwargs):
        return self.rename_bot_top.get()

    def selectionMenu(self, *args, **kwargs):
        """Selection Menu Dropdown"""
        # Create the menu
        self.selection_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Select All
        self.selection_menu.add_command(
            label="Select All",
            command=bpn.fn_treeview.selectAll,
            accelerator="Ctrl+A",
        )

        # Deselect All
        self.selection_menu.add_command(
            label="Deselect All",
            command=bpn.fn_treeview.deselectAll,
            accelerator="Ctrl+D",
        )

        # Invert Selection
        self.selection_menu.add_command(
            label="Invert Selection",
            command=bpn.fn_treeview.invertSelection,
            accelerator="Ctrl+I",
        )

    def commandMenu(self, *args, **kwargs):
        """Command Menu Dropdown"""
        # Variable defs
        self.selected_command = tk.StringVar(value="DEFAULT")

        # Create the menu
        self.command_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # Save current variable values entries as command
        self.command_menu.add_command(
            label="Save Field States to Command",
            command=commands.SaveCommandNameWindow,
        )

        # Load selected command
        self.command_menu.add_command(
            label="Load Field States from Command",
            command=commands.load_command_call,
            accelerator="Ctrl+E",
        )

        # Apply selected command
        self.command_menu.add_command(
            label="Apply Selected Command",
            command=rename.apply_command,
            accelerator="Ctrl+Y",
        )

        # Delete selected command
        self.command_menu.add_command(
            label="Delete Selected Command", command=commands.delete_command
        )

        self.command_select_menu = tk.Menu(
            self.command_menu, tearoff=0, bg="gray75", foreground="black"
        )

        # Only try to load the commands if there is a path to the
        # commands configuration file
        if bpn.CONFIG_FOLDER_PATH:
            self.updateCommandListMenu()

        # Separator
        self.command_menu.add_separator()

        # Apply selected command
        self.command_menu.add_cascade(
            label="Select Command", menu=self.command_select_menu
        )

    def updateCommandListMenu(self, *args, **kwargs):
        """Deletes the already existing items and updates the view"""
        self.command_select_menu.delete(0, "end")
        # Read the commands config and create a radio button for each command
        for command_name in bpn.COMMAND_CONF.sections():
            self.command_select_menu.add_radiobutton(
                label=command_name,
                variable=self.selected_command,
                value=command_name,
            )

    def aboutMenu(self, *args, **kwargs):
        """About Menu Dropdown"""
        # Create the menu
        self.about_menu = tk.Menu(
            self, tearoff=0, bg="gray75", foreground="black"
        )

        # GitHub
        self.about_menu.add_command(
            label="Project", command=self.openProjectUrl
        )

        # Wiki
        self.about_menu.add_command(label="Help", command=self.openWikiUrl)

    def renameEnable(self, *args, **kwargs):
        """Enable the rename menu options when on the rename page"""
        self.file_menu.entryconfigure(index=0, state="active")
        self.file_menu.entryconfigure(index=1, state="active")
        self.file_menu.entryconfigure(index=2, state="active")

    def renameDisable(self, *args, **kwargs):
        """Disable the rename menu options when not in the rename page"""
        self.file_menu.entryconfigure(index=0, state="disable")
        self.file_menu.entryconfigure(index=1, state="disable")
        self.file_menu.entryconfigure(index=2, state="disable")

    def metadataEnable(self, *args, **kwargs):
        """Enable the metadata menu options when on the metadata page"""
        if bpn.METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state="active")
            self.file_menu.entryconfigure(index=6, state="active")
            self.file_menu.entryconfigure(index=7, state="active")
            self.file_menu.entryconfigure(index=8, state="active")
            self.file_menu.entryconfigure(index=9, state="active")

    def metadataDisable(self, *args, **kwargs):
        """Disable the metadata menu options when not in the metadata page"""
        if bpn.METADATA_IMPORT:
            self.file_menu.entryconfigure(index=5, state="disable")
            self.file_menu.entryconfigure(index=6, state="disable")
            self.file_menu.entryconfigure(index=7, state="disable")
            self.file_menu.entryconfigure(index=8, state="disable")
            self.file_menu.entryconfigure(index=9, state="disable")

    def selectedCommandGet(self, *args, **kwargs):
        """Return the selected command name"""
        return self.selected_command.get()

    def openProjectUrl(self, *args, **kwargs):
        """Open the Project Url"""
        webbrowser.open(PROJECT_URL)

    def openWikiUrl(self, *args, **kwargs):
        """Open the Wiki Url"""
        webbrowser.open(WIKI_URL)
