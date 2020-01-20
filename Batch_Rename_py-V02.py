#!/usr/bin/python

import os
import shutil

import string
import unicodedata
import re               # regular expressions

import mutagen
from mutagen.flac import FLAC

from io import BytesIO
import PIL.ImageTk
import PIL

import tkinter as tk
from tkinter import ttk


###############################################################################
'''
    INDEX:
        - Vertical Scrollable Frame

        - Tree System Navigation
        - File Folder Navigation
        - Directory entry for File Folder Navigation
        - Notebook
        - Extra Information Bar

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

        - General functions

        - Main function

    KNOWN BUGS:
        None so far
'''
###############################################################################


###################################
'''
    GLOBAL CONSTANTS
'''
###################################

APP_NAME = 'Batch Renamer'
APP_VER = 2.00
TITLE = '{}-V{}'.format(APP_NAME, APP_VER)

PATH = '/'


###################################
'''
    WIDGET CREATION CLASSES
'''
###################################

class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand='false')
        canvas = tk.Canvas(self, bd=0, background='gray85', highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
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


###################################
'''
    BASIC WIDGET CLASSES
'''
###################################

class TreeNavigator:
    def __init__(self, master, path, *args, **kwargs):
        self.path = path

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
        self.tree_nav.column('#0', width=250)
        # Treeview and the scrollbars placing
        self.tree_nav.grid(row=0, column=0)
        ysb_tree_nav.grid(row=0, column=1, sticky='ns')
        xsb_tree_nav.grid(row=1, column=0, sticky='ew')
        # Initialization
        self.basicPopulation()

        self.bindEntries()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # Tree navigation bindings
        self.tree_nav.bind('<<TreeviewOpen>>', self.Open_Node)
        self.tree_nav.bind('<<TreeviewSelect>>', TreeNav_Select_Calls)

    def basicPopulation(self, *args, **kwargs):
        # Create a dict of what nodes exist. Used to load the placeholder nodes
        self.nodes = dict()

        # Delete all children and reset Treeview
        for child in self.tree_nav.get_children():
            self.tree_nav.delete(child)

        # Load folders and insert nodes
        directories, files = Load_Child(self.path)
        for a in directories:
            self.insertNode('', a, os.path.join(self.path, a))

    def selectedItem(self, *args, **kwargs):
        # Since this tree can only select 1 item at a time we just pass
        # the index instead of doing a for loop
        return self.tree_nav.selection()[0]

    def insertNode(self, parent, text, abspath, *args, **kwargs):
        ''' Create nodes for the tree file navigation. '''
        # uses the absolute path to the folder as the iid
        node = self.tree_nav.insert(
                                    parent=parent,
                                    index='end',
                                    iid=abspath,
                                    text=text,
                                    open=False
                                    )
        # make dirs openable without loading children
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree_nav.insert(node, 'end')


    def Open_Node(self, *args, **kwargs):
        ''' Open Node action. Only avaible to the tree file navigation. '''
        # get active node
        node = self.tree_nav.focus()
        # get the path to the directory of the opening node
        abspath = self.nodes.pop(node, None)
        if abspath:
            # delete the placeholder node that was created previously
            self.tree_nav.delete(self.tree_nav.get_children(node))
            directories, files = Load_Child(abspath)
            # check if the opened folder has any files or directories
            # if it doesn't, add an empty node
            if files:
                # inserts only the directories
                # because we dont want to show the files in this treeview
                for item in directories:
                    self.insertNode(
                                                node,
                                                item,
                                                os.path.join(abspath, item)
                                                )
            else:   # for empty folders
                self.insertNode(
                                            node,
                                            '(empty)',
                                            os.path.join(abspath, '(empty)')
                                            )

    def openFolderTreeNav(self, *args, **kwargs):
        folder_path = self.selectedItem()
        fn_treeview.openFolder(folder_path)

    def updateNode(self, *args, **kwargs):
        '''
            Updates the focused node.
            Deletes all children and inserts an empty node
        '''
        path = self.tree_nav.focus()
        children = self.tree_nav.get_children(path)
        for child in children:
            self.tree_nav.delete(child)

        # reinsert an empty node
        self.tree_nav.insert(path, 'end')
        self.nodes[path] = path


class FileNavigator:
    '''
        Draws the treeview of the file navigation:
            It exclusively shows folders.
            You can only select one item at a time.
            It creates a temporary child node (empty) inside the folders to be
            able to open them without having to load the directories inside.
            If this wasn't done the app would have to load the whole system
            at starup.
        Draws the treeview of the files and folders inside the selected folder.
    '''
    def __init__(self, master, *args, **kwargs):
        frame = ttk.Frame(master)
        frame.grid(row=1, column=1)

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
        # Create and name columns for the tree selected folder
        self.tree_folder.heading('#0', text='Old Name', anchor='w')
        self.tree_folder['columns'] = ('#1')
        self.tree_folder.column('#0', width=250)
        self.tree_folder.column('#1', width=250)
        self.tree_folder.heading('#1', text='New name', anchor='w')
        # Treeview and the scrollbars placing
        self.tree_folder.grid(row=0, column=2)
        ysb_tree_folder.grid(row=0, column=3, sticky='ns')
        xsb_tree_folder.grid(row=1, column=2, sticky='ew')

        # Bindings
        self.bindEntries()

    def oldNameGet(self, item, *args, **kwargs):
        return fn_treeview.tree_folder.item(item)['text']

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # File Navigation bindings
        # calls to update the new name column
        self.tree_folder.bind('<<TreeviewSelect>>', Populate_Fields)
        self.tree_folder.bind('<<TreeviewSelect>>', Call_For_Info_Bar, add='+')
        self.tree_folder.bind('<Button-3>', self.rightClickPathToClip)

    def insertNode(self, text, abspath, *args, **kwargs):
        ''' Create nodes '''
        # uses the absolute path to the folder as the iid
        node = self.tree_folder.insert(
                                        parent='',
                                        index='end',
                                        iid=abspath,
                                        text=text,
                                        values=[text],
                                        open=False
                                        )

    def openFolder(self, folder_path, *args, **kwargs):
        ''' Loads the treeview of the files inside the selected folder '''
        self.childrenDeleteAll()
        # load the directories and add them
        directories, files = Load_Child(folder_path)
        for a in files:
            self.insertNode(a, os.path.join(folder_path, a))

    def childrenDeleteAll(self, *args, **kwargs):
        ''' Delete already existing nodes in the folder view '''
        to_delete = self.tree_folder.get_children()
        for item in to_delete:
            self.tree_folder.delete(item)

    def setNewName(self, path, new_name, *args, **kwargs):
        return self.tree_folder.set(path, '#1', new_name)

    def selectedItems(self, *args, **kwargs):
        return self.tree_folder.selection()

    def rightClickPathToClip(self, event, *args, **kwargs):
        '''
            When you right click over an item in the folder treeview gets the
            path to that item and puts it in the clipboard so you can paste it
            somewhere elese.
        '''
        path = self.tree_folder.identify_row(event.y)
        root.clipboard_clear()
        root.clipboard_append(path)

    def resetNewName(self, *args, **kwargs):
        '''
            Renames every item to their old name, so if you change selection
            they dont still show the new name.
        '''
        all_nodes = self.tree_folder.get_children()
        for item in all_nodes:
            old_name = self.oldNameGet(item)
            self.setNewName(item, old_name)

    @staticmethod
    def Show_New_Name(*args, **kwargs):
        '''
            Iterates over each selected item and recreates each new name
            following the renaming rules given inside the rename page of
            the notebook.
        '''
        # get list of selected items iids
        selection = fn_treeview.selectedItems()
        sel_item = 0   # the index of the selected item, used for numbering
        for path in selection:
            # get the old name
            old_name = fn_treeview.oldNameGet(path)
            # transform the old name to the new name
            new_name = New_Naming(old_name, sel_item, path)
            # changes the new name column
            fn_treeview.setNewName(path, new_name)

            sel_item += 1


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
                                                    command=folder_treeview.basicPopulation
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
        pass

    def folderDirSet(self, *args, **kwargs):
        folder_path = folder_treeview.selectedItem()
        self.folder_dir.set(folder_path)

    def openFolderTreeNav(self, *args, **kwags):
        folder_path = self.folderDirGet()
        if os.path.isdir(folder_path):
            fn_treeview.openFolder(folder_path)
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
        self.nb_metadata = ttk.Frame(self.nb)
        # Add the pages
        self.nb.add(self.nb_rename, text='Rename')
        self.nb.add(self.nb_metadata, text='Metadata')

        # Call the widgets that go inside each page
        self.renameNbPage(self.nb_rename)
        self.metadataNbPage(self.nb_metadata)

        # Bindings
        self.bindEntries()

    def renameNbPage(self, master, *args, **kwargs):
        ''' Calls to draw the rename widgets '''
        self.nb_rename_frame = ttk.Frame(master)
        self.nb_rename_frame.grid(sticky='nsew')

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
        # Rename (last)
        self.rename = Rename(self.nb_rename_frame)

        # Add a little bit of padding between each widget
        for child in self.nb_rename_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)


    def metadataNbPage(self, master, *args, **kwargs):
        ''' Calls to draw the matadata widgets '''
        self.nb_metadata_frame = ttk.Frame(master)
        self.nb_metadata_frame.grid(sticky='nsew')

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

class Reg_Exp:    # (1)
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Regular Expressions (1)')
        self.lf.grid(column=0, row=0, sticky='nsew')

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
        self.reset_button.grid(column=2, row=2, sticky='w')

        self.bindEntries()

    def matchRegGet(self, *args, **kwargs):
        return self.match_reg.get()

    def replaceWithGet(self, *args, **kwargs):
        return self.replace_with.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # calls to update the new name column
        self.match_reg.trace_add('write', FileNavigator.Show_New_Name)
        self.replace_with.trace_add('write', FileNavigator.Show_New_Name)

    def extendedRegExp(self, *args, **kwargs):
        '''
            Create a pop up window with extended entries for the
            regular expressions and a button 'Done' that saves the changes
        '''
        self.ex_w_frame = Toplevel(root)
        self.ex_w_frame.title('Extended Regular Expression Window')
        self.ex_w_frame.attributes('-type', 'dialog')

        # Extended Match, text
        ttk.Label(self.ex_w_frame, text="Match").grid(column=0, row=0, sticky='w')
        self.ex_match_reg_text = Text(self.ex_w_frame)
        self.ex_match_reg_text.grid(column=0, row=1, sticky='ew')
        self.ex_match_reg_text.insert('end', self.matchRegGet())

        # Extended Replace, text
        ttk.Label(self.ex_w_frame, text="Replace").grid(column=0, row=2, sticky='w')
        self.ex_replace_with_text = Text(self.ex_w_frame)
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

        # remove the newline char
        ex_match_reg = ex_match_reg[:-1]
        ex_replace_with = ex_replace_with[:-1]

        # save to variable
        self.match_reg.set(ex_match_reg)
        self.replace_with.set(ex_replace_with)

        # kill window
        self.ex_w_frame.destroy()
    
    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.match_reg.set('')
        self.replace_with.set('')

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

                try:    # prevent IndexError blocking
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
        self.lf.grid(column=0, row=1, sticky='nsew')

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
        self.reset_button.grid(column=2, row=2, sticky='w')

        self.bindEntries()

    def nameOptGet(self, *args, **kwargs):
        return self.name_opt.get()

    def fixedNameGet(self, *args, **kwargs):
        return self.fixed_name.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''

        self.name_opt_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.name_opt.trace_add('write', FileNavigator.Show_New_Name)
        self.fixed_name.trace_add('write', FileNavigator.Show_New_Name)

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


class Replace:    # (3)
    '''
        Draws the replace widget. Inside rename notebook. 3rd thing to change.
        It has:
            - Entry to choose char(s) to replace
            - Entry for what to replace those char(s) with
            - Reset button
    '''
    def __init__(self, master, *args, **kwargs):        
        self.lf = ttk.Labelframe(master, text='Replace (3)')
        self.lf.grid(column=1, row=0, sticky='nsew')

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
        self.reset_button.grid(column=2, row=2, sticky='w')

        self.bindEntries()

    def replaceThisGet(self, *args, **kwargs):
        return self.replace_this.get()

    def replaceWithGet(self, *args, **kwargs):
        return self.replace_with.get()

    def matchCaseGet(self, *args, **kwargs):
        return self.match_case.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        # calls to update the new name column
        self.replace_this.trace_add('write', FileNavigator.Show_New_Name)
        self.replace_with.trace_add('write', FileNavigator.Show_New_Name)
        self.match_case.trace_add('write', FileNavigator.Show_New_Name)
    
    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.replace_this.set('')
        self.replace_with.set('')
        self.match_case.set(False)

    @staticmethod
    def Replace_Action(name, *args, **kwargs):
        ''' Does the replace action for the new name '''
        replace_this = nb.replace.replaceThisGet()
        replace_with = nb.replace.replaceWithGet()
        match_case = nb.replace.matchCaseGet()

        if match_case:
            name = name.replace(replace_this, replace_with)
        elif replace_this != '':    # if replace_this is empty it breaks
            idx = name.lower().find(replace_this.lower())
            while idx != -1:
                name = (name[:idx] + replace_with +
                        name[idx + len(replace_this):])
                idx = idx + len(replace_with)

                idx = name.lower().find(replace_this.lower(), idx)

        return name

class Case:   # (4)
    '''
        Draws the Case changer widget. Inside rename notebook.
        4th thing to change.
        It has:
            - Combobox to choose what case to use (same, upper, lower, title)
            - Reset button
    '''
    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text='Case (4)')
        self.lf.grid(column=1, row=1, sticky='nsew')

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
        self.reset_button.grid(column=2, row=2, sticky='w')

        self.bindEntries()

    def caseWantGet(self, *args, **kwargs):
        return self.case_want.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''
        self.case_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.case_want.trace_add('write', FileNavigator.Show_New_Name)

    def defocus(self, *args, **kwargs):
        '''
            Clears the highlightning of the comboboxes inside this frame
            whenever any of them changes value.
        '''
        self.case_combo.selection_clear()

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget '''
        self.case_want.set('Same')

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


class Remove:     # (5)
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
        self.lf.grid(column=2, row=0, rowspan=2, sticky='nsew')

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
                                    to=500,
                                    textvariable=self.first_n
                                    )
        self.first_n_spin.grid(column=1, row=0)

        # Remove las n characters, spinbox
        ttk.Label(self.lf, text='Last n').grid(column=2, row=0, sticky='ew')
        self.last_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=500,
                                    textvariable=self.last_n
                                    )
        self.last_n_spin.grid(column=3, row=0)

        # Remove from this char position, spinbox
        ttk.Label(self.lf, text='From').grid(column=0, row=1, sticky='ew')
        self.from_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=500,
                                    textvariable=self.from_n
                                    )
        self.from_n_spin.grid(column=1, row=1)

        # Remove to this char position, spinbox
        ttk.Label(self.lf, text='To').grid(column=2, row=1, sticky='ew')
        self.to_n_spin = ttk.Spinbox(
                                    self.lf,
                                    width=3,
                                    to=500,
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
        self.reset_button.grid(column=20, row=20, sticky='w')

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
        # when updating from_n value makes sure its not bigger than to_n
        self.from_n.trace_add('write', self.fromAddTo)
        self.to_n.trace_add('write', self.fromAddTo)
        # defocus the hightlight when changing combobox
        self.lead_dots_combo.bind('<<ComboboxSelected>>', self.defocus)
        self.crop_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.first_n.trace_add('write', FileNavigator.Show_New_Name)
        self.last_n.trace_add('write', FileNavigator.Show_New_Name)
        self.from_n.trace_add('write', FileNavigator.Show_New_Name)
        self.to_n.trace_add('write', FileNavigator.Show_New_Name)
        self.rm_words.trace_add('write', FileNavigator.Show_New_Name)
        self.rm_chars.trace_add('write', FileNavigator.Show_New_Name)
        self.crop_pos.trace_add('write', FileNavigator.Show_New_Name)
        self.crop_this.trace_add('write', FileNavigator.Show_New_Name)
        self.digits.trace_add('write', FileNavigator.Show_New_Name)
        self.d_s.trace_add('write', FileNavigator.Show_New_Name)
        self.accents.trace_add('write', FileNavigator.Show_New_Name)
        self.chars.trace_add('write', FileNavigator.Show_New_Name)
        self.sym.trace_add('write', FileNavigator.Show_New_Name)
        self.lead_dots.trace_add('write', FileNavigator.Show_New_Name)

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

    @staticmethod
    def Remove_N_Chars(name, *args, **kwargs):
        ''' Removes chars depending on their index '''
        first_n = nb.remove.firstNGet()
        # need this to be a negattive number
        last_n = -nb.remove.lastNGet()
        # need this to be one less of the displayed number
        from_n = nb.remove.fromNGet() - 1
        to_n = nb.remove.toNGet()

        name = name[first_n:]
        if last_n != 0:     # only act when the index is not 0
            name = name[:last_n]
        if from_n != -1:    # only act when the index is not -1
            # doing it like this is way faster than transforming it to a list
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
        try:    # if the value doesnt exist it raises a ValueError
            # needs the while to remove all ocurences of the word
            while rm_words in name: name.remove(rm_words)
        except ValueError:
            pass        
        name = ' '.join(name)

        # removes every apparition of all chars in the str by themselves
        for chara in rm_chars:
            name = name.replace(chara, '')

        return name

    @staticmethod
    def Crop_Remove(name, *args, **kwargs):
        '''
            Crops before or after the specified char(s).
            It can also crop inbetween 2 char(s), ex: \[*\] a*a
        '''
        crop_pos = nb.remove.cropPosGet()
        crop_this = nb.remove.cropThisGet()

        if crop_this != '':     # if this field is empty do nothing
            # if the combobox is not in 'Special' do the regular crops
            if crop_pos != 'Special':
                name_tuple = name.partition(crop_this)
                if crop_pos == 'Before':
                    name = name_tuple[2]
                elif crop_pos == 'After':
                    name = name_tuple[0]
            else:
                # create a regular expresion from the given string
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


class Move_Copy_Parts:    # (6)
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
        self.lf.grid(column=0, row=2, columnspan=2, sticky='nsew')

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
                                    to=500,
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
                                    to=500,
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
        self.reset_button.grid(column=10, row=1, sticky='w')

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
        self.ori_pos.trace_add('write', FileNavigator.Show_New_Name)
        self.ori_n.trace_add('write', FileNavigator.Show_New_Name)
        self.end_pos.trace_add('write', FileNavigator.Show_New_Name)
        self.end_n.trace_add('write', FileNavigator.Show_New_Name)
        self.sep.trace_add('write', FileNavigator.Show_New_Name)

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


class Add_To_String:  # (7)
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
        self.lf.grid(column=3, row=0, rowspan=2, sticky='nsew')

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
                                    from_=-500,
                                    to=500,
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
        self.reset_button.grid(column=20, row=20, sticky='w')

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
        self.prefix.trace_add('write', FileNavigator.Show_New_Name)
        self.insert_this.trace_add('write', FileNavigator.Show_New_Name)
        self.at_pos.trace_add('write', FileNavigator.Show_New_Name)
        self.suffix.trace_add('write', FileNavigator.Show_New_Name)
        self.word_space.trace_add('write', FileNavigator.Show_New_Name)

    def resetWidget(self, *args, **kwargs):
        ''' Resets each and all data variables inside the widget. '''
        self.prefix.set('')
        self.insert_this.set('')
        self.at_pos.set(0)
        self.suffix.set('')
        self.word_space.set(False)

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
            name = "".join([" " + ch if ch.isupper() else ch for ch in name])

        return name


class Append_Folder_Name: # (8)
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
        self.lf.grid(column=2, row=2, columnspan=2, sticky='nsew')

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
        self.reset_button.grid(column=20, row=20, sticky='w')

        self.bindEntries()

    def namePosGet(self, *args, **kwargs):
        return self.name_pos.get()

    def sepGet(self, *args, **kwargs):
        return self.sep.get()

    def levelsGet(self, *args, **kwargs):
        return self.levels.get()

    def bindEntries(self, *args, **kwargs):
        ''' What to execute when the bindings happen. '''
        # defocus the hightlight when changing combobox
        self.name_pos_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.name_pos.trace_add('write', FileNavigator.Show_New_Name)
        self.sep.trace_add('write', FileNavigator.Show_New_Name)
        self.levels.trace_add('write', FileNavigator.Show_New_Name)

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
                name = name[:-len(sep)]    # remove the extra trailing separator

        return name


class Numbering:  # (9)
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
        self.lf.grid(column=4, row=0, rowspan=2, sticky='nsew')

        # Variable defs
        self.mode = tk.StringVar()
        self.at_n = tk.IntVar()
        self.start_num = tk.IntVar()
        self.incr_num = tk.IntVar()
        self.pad = tk.IntVar()
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
                                    from_=-500,
                                    to=500,
                                    textvariable=self.at_n
                                    )
        self.at_n_spin.grid(column=3, row=0)
        self.at_n.set(0)

        # Start from this number, spinbox
        ttk.Label(self.lf, text='Start').grid(column=0, row=1, sticky='ew')
        self.start_num_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        to=500,
                                        textvariable=self.start_num
                                        )
        self.start_num_spin.grid(column=1, row=1)

        # Step, spinbox
        ttk.Label(self.lf, text='Incr.').grid(column=2, row=1, sticky='ew')
        self.incr_num_spin = ttk.Spinbox(
                                        self.lf,
                                        width=3,
                                        from_=1,
                                        to=500,
                                        textvariable=self.incr_num
                                        )
        self.incr_num_spin.grid(column=3, row=1)

        # Padding of possible 0s, spinbox
        ttk.Label(self.lf, text='Pad').grid(column=0, row=2, sticky='ew')
        self.pad_spin = ttk.Spinbox(
                                self.lf,
                                width=3,
                                from_=1,
                                to=500,
                                textvariable=self.pad
                                )
        self.pad_spin.grid(column=1, row=2)

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
        self.type_base_combo['value']=(
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
        self.reset_button.grid(column=20, row=20, sticky='w')

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
        self.mode.trace_add('write', FileNavigator.Show_New_Name)
        self.at_n.trace_add('write', FileNavigator.Show_New_Name)
        self.start_num.trace_add('write', FileNavigator.Show_New_Name)
        self.incr_num.trace_add('write', FileNavigator.Show_New_Name)
        self.pad.trace_add('write', FileNavigator.Show_New_Name)
        self.sep.trace_add('write', FileNavigator.Show_New_Name)
        self.type_base.trace_add('write', FileNavigator.Show_New_Name)

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

    @staticmethod
    def Numbering_Rename(name, sel_item, *args, **kwargs):
        ''' Calls to create the numbering and then sets it up inplace '''
        mode = nb.numbering.modeGet()
        at_n = nb.numbering.atNGet()
        start_num = nb.numbering.startNumGet()
        incr_num = nb.numbering.incrNumGet()
        sep = nb.numbering.sepGet()

        # calculate what number we are in taking into account the step and
        # the starting number
        n = sel_item + start_num + (incr_num - 1) * sel_item
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
            l = ''
            for a in range(0, cycle + 1):
                l = l + string.ascii_lowercase[n - 26 * cycle]
            n = l.rjust(pad, 'a')

            if type_base == 'Upper Case Letters':
                n = n.upper()

        return n


class Extension_Rep:  # (10)
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
        self.lf.grid(column=4, row=2, sticky='nsew')

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
        self.reset_button.grid(column=2, row=2, sticky='w')

        self.bindEntries()

    def changeExtGet(self, *args, **kwargs):
        return self.change_ext.get()

    def fixedExtGet(self, *args, **kwargs):
        return self.fixed_ext.get()

    def bindEntries(self, *args, **kwargs):
        ''' Defines the binded actions '''

        self.change_ext_combo.bind('<<ComboboxSelected>>', self.defocus)

        # calls to update the new name column
        self.change_ext.trace_add('write', FileNavigator.Show_New_Name)
        self.fixed_ext.trace_add('write', FileNavigator.Show_New_Name)

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
        self.frame.grid(column=4, row=3, columnspan=3, sticky='e')

        self.reset_button = ttk.Button(
                                        self.frame,
                                        text="Reset",
                                        command=self.fullReset
                                        )
        self.reset_button.grid(column=0, row=0, padx=1, pady=1)

        self.revert_button = ttk.Button(
                                        self.frame,
                                        text="Revert",
                                        command=self.revert
                                        )
        self.revert_button.grid(column=0, row=1, padx=1, pady=1)

        self.rename_button = ttk.Button(
                                        self.frame,
                                        text="Rename",
                                        command=self.Final_Rename
                                        )
        self.rename_button.grid(column=1, row=0, rowspan=2,
                                padx=1, pady=1, sticky='ns'
                                )

    def fullReset(self, *args, **kwargs):
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

    def revert(self, *args, **kwargs):
        # dirs_select = FileListing.tree.curselection()
        # for i in dirs_select:
        #     print(i)
        inf_bar.lastActionRefresh('Revert')

    @staticmethod
    def Final_Rename(*args, **kwargs):
        sel_paths = fn_treeview.selectedItems()
        for path in sel_paths:
            name = fn_treeview.tree_folder.set(path, '#1')
            System_Rename(path, name)

        inf_bar.lastActionRefresh('Finished Rename')

        # get the folder path and update the treeview
        folder_path = path.rpartition('/')[0]
        fn_treeview.openFolder(folder_path)

        # update the folder view
        folder_treeview.updateNode()


###################################
'''
    METADATA CLASSES
'''
###################################

class Metadata_ListEntries:
    def __init__(self, master, *args, **kwargs):
        self.frame = VerticalScrolledFrame(master)
        self.frame.grid(column=0, row=0, sticky='ns')

        self.metaDictReset()

        self.metadataEntriesCreate()

    def metaDictTextGet(self, key, *args, **kwargs):
        return self.meta_dict[key].get()

    def metaDictGet(self, *args, **kwargs):
        return self.meta_dict

    def metaDictReset(self, *args, **kwargs):
        self.meta_dict = {'title':tk.StringVar(), 'tracknumber':tk.StringVar(),
                            'artist':tk.StringVar(), 'album':tk.StringVar(),
                            'date':tk.StringVar(), 'genre':tk.StringVar()}

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
        self.meta_dict = {'title':[], 'tracknumber':[], 'artist':[],
                            'album':[], 'date':[], 'genre':[]}
        try:
            for file in selection:
                meta_audio = Meta_Audio(file)

                for meta_item in meta_audio:
                    listed_value = list()
                    meta_value = meta_audio.get(meta_item)

                    # adds to each key the value for this selected item
                    self.meta_dict[meta_item] = (
                                        self.meta_dict.get(meta_item, list()) +
                                        meta_value
                                        )

            for key in self.meta_dict:
                # remove duplicates
                self.meta_dict[key] = noDuplicatesList(self.meta_dict[key])
                # list to string
                str_value = self.metaValuesListToStr(self.meta_dict[key])

                # set each key value to a StringVar
                self.meta_dict[key] = tk.StringVar(value=str_value)

            return self.meta_dict

        except TypeError as e:
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
        for child in self.frame.interior.winfo_children():
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
        n = 0
        for key in self.meta_dict:
            ttk.Label(self.frame.interior, text=key).grid(
                                                        column=0,
                                                        row=n,
                                                        sticky='e'
                                                        )
            ttk.Entry(
                        self.frame.interior,
                        width=50,
                        textvariable=self.meta_dict[key]
                        ).grid(column=1, row=n, sticky='ew')

            n += 1


class Metadata_Img:
    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=1, row=0)

        self.photo_image = tk.PhotoImage() # empty photo image to force the
                                        # label to use pixel size
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
        try: # error handling if theres no image
            selection = fn_treeview.selectedItems()
            file = selection[0]
            meta_audio = Meta_Audio(file)
            # loads a first image
            self.picture = meta_audio.pictures[0].data

            for file in selection:
                meta_audio = Meta_Audio(file)
                img_comparison = meta_audio.pictures[0].data

                # checks against that first loaded image every other
                # image in the selection. Becomes true when any of the other
                # images are different
                if img_comparison != self.picture:
                    self.picture = None
                    self.size_label.config(text='Different images')

                    break

        except (IndexError, AttributeError) as e:
            # set the size labe to show theres no image
            self.size_label.config(text='No image')

    def imageShow(self, *args, **kwargs):
        ''' Shows the first image binded to the files '''
        self.picture = None
        self.imageLoad()
        if self.picture != None:
            im = PIL.Image.open(BytesIO(self.picture))
            # get image size before resizing
            im_width, im_height = map(str, im.size)

            # resize
            im = im.resize((250, 250), PIL.Image.ANTIALIAS)

            # show image
            render = PIL.ImageTk.PhotoImage(im)
            self.img.image = render
            self.img.config(image=render)

            # show image size
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
        self.apply_meta_button.grid(column=0, row=0, sticky='w')

        self.apply_img_button = ttk.Button(
                                    self.frame,
                                    width=10,
                                    text="Apply Img",
                                    command=self.imgChangesCall
                                    )
        self.apply_img_button.grid(column=0, row=1, sticky='w')

        self.apply_all_button = ttk.Button(
                                    self.frame,
                                    width=10,
                                    text="Apply All",
                                    command=self.allChangesCall
                                    )
        self.apply_all_button.grid(column=0, row=2, sticky='w')

    def metaChangesCall(self, *args, **kwargs):
        '''
            Calls the procedure to only change metadata tags.
            Loads the new values from the list of entries and sets them up.
        '''
        selection = fn_treeview.selectedItems()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Delete the last action text from the info bar
        inf_bar.lastActionRefresh('')

        for item in selection:
            meta_audio = Meta_Audio(item)
            for key in meta_dict:
                value = nb.metadata_list_entries.metaDictTextGet(key)

                self.applyMetaChanges(meta_audio, key, value)

        # Show that its finish by setting the info bar message.
        inf_bar.lastActionRefresh('Metadata Changed')

    def applyMetaChanges(self, meta_audio, key, value, *args, **kwargs):
        '''
            Applies the changes to the metadata. Skips the instances where
            there are several values (so as not to set all values to every
            item) and removes empty tags (if they also exist in the metadata
            tags of the item).
        '''
        # if there is more than one value for the field, skip it
        if ';' not in value:
            if value:
                meta_audio[key] = value
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

        # Delete the last action text from the info bar
        inf_bar.lastActionRefresh('')

        if img_path.endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
            # Load the new image
            img = self.loadImage(img_path)
            for item in selection:
                # Load the item metadata and set the new picture.
                meta_audio = Meta_Audio(item)
                self.applyImgChanges(meta_audio, img)

        # Show that its finish by setting the info bar message.
        inf_bar.lastActionRefresh('Image Changed')

    def loadImage(self, img_path, *args, **kwargs):
        '''
            Creates a mutagen.flac.Picture object, sets its mimetype, its
            type and its description. Then loads the selected img and returns
            the Picture object.
        '''
        # create img object and set its properties
        img = mutagen.flac.Picture()
        # type 3 is for cover image
        img.type = 3
        # Set the corresponding mime type
        if img_path.endswith('png'):
            img.mime = 'image/png'
        else:
            img.mime = 'image/jpg'
        # Set description
        img.desc = 'front cover'
        img.data = open(img_path, 'rb').read()

        return img

    def applyImgChanges(self, meta_audio, img, *args, **kwargs):
        ''' Changes the image of a flac audio file '''
        meta_audio.clear_pictures()     # clear other images
        meta_audio.add_picture(img)     # set new image
        meta_audio.save()
                
    def allChangesCall(self, *args, **kwargs):
        ''' Calls to both the metadata change and the image change '''
        selection = fn_treeview.selectedItems()
        img_path = nb.metadata_img.imagePathGet()
        meta_dict = nb.metadata_list_entries.metaDictGet()

        # Delete the last action text from the info bar
        inf_bar.lastActionRefresh('')

        if img_path.endswith(('jpg', 'jpeg', 'png')) and os.path.exists(img_path):
            img = self.loadImage(img_path)
            for item in selection:
                meta_audio = Meta_Audio(item)

                # Change the image
                self.applyImgChanges(meta_audio, img)

                # Change the metadata tags
                for key in meta_dict:
                    value = nb.metadata_list_entries.metaDictTextGet(key)
                    
                    self.applyMetaChanges(meta_audio, key, value)

        # Show that its finish by setting the info bar message.
        inf_bar.lastActionRefresh('Metadata and Image Changed')



###################################
'''
    GENERAL FUNCTIONS
'''
###################################

def Load_Child(path, *args, **kwargs):
    '''
        Loads the directories inside the folder given by "path".
        Separates the output in files and directories.
        If unable to open raise an exception.
    '''
    directories = []
    files = []
    try:
        # separate dirs and files
        for a in os.listdir(path):
            # bug where it will get stuck in /home/Earth (NAS) when it cant
            # access it
            abs_path = os.path.join(path, a)
            if os.path.isdir(abs_path):
                directories.append(a)
            else:
                files.append(a)
    except OSError as e:
        directories = ['Unable to Open']
        files = []
        pass

    # sort dirs and files alphabetically
    directories.sort()
    files.sort()

    files = directories + files

    return directories, files

def Populate_Fields(*args, **kwargs):
    tab = nb.nbTabGet()

    if tab == 'Rename':
        fn_treeview.resetNewName()
        FileNavigator.Show_New_Name()
    elif tab == 'Metadata':
        fn_treeview.resetNewName()
        nb.metadata_list_entries.metadataSelect()
        nb.metadata_img.imageShow()

def noDuplicatesList(list_convert, *args, **kwargs):
    return list(dict.fromkeys(list_convert))

def Meta_Audio(file):
    if '.flac' in file:
        meta_audio = FLAC(file)
    elif '.mp3' in file:
        meta_audio = MP3(file)
    else:
        meta_audio = None

    return meta_audio

def TreeNav_Select_Calls(*args, **kwargs):
    folder_treeview.openFolderTreeNav()
    inf_bar.numItemsRefresh()
    dir_entry_frame.folderDirSet()

def Call_For_Info_Bar(*args, **kwargs):
    inf_bar.numItemsRefresh()

def New_Naming(name, sel_item, path, *args, **kwargs):
    '''
        Creates the new name going through all fields and making the changes
        to the old_name string
    '''
    # separate name and extension
    name, ext = De_Ext(name)

    name = Reg_Exp.Reg_Exp_Rename(name)                         # (1)
    name = Name_Basic.Name_Basic_Rename(name)                   # (2)
    name = Replace.Replace_Action(name)                         # (3)
    name = Case.Case_Change(name)                               # (4)
    name = Remove.Remove_Rename(name)                           # (5)
    name = Move_Copy_Parts.Move_Copy_Action(name)               # (6)
    name = Add_To_String.Add_Rename(name)                       # (7)
    name = Append_Folder_Name.Append_Folder_Rename(name, path)  # (8)
    name = Numbering.Numbering_Rename(name, sel_item)           # (9)

    ext = Extension_Rep.Extension_Rename(ext)                   # (10)

    # remove leading and trailing whitespaces and re-add the extension
    name = name.strip() + ext

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

def System_Rename(file, name, *args, **kwargs):
    ''' Changes the name of the files in the system '''
    path_tuple = file.rpartition('/')
    new_path = path_tuple[0] + path_tuple[1] + name
    if not os.path.exists(new_path):
        # os.rename(file, name)
        shutil.move(file, new_path)

        print('Rename {} to {}'.format(file, new_path))

    else:
        inf_bar.lastActionRefresh("Couldn't Rename file. Path already exists")



'''
    INITIALIZATION OF THE WINDOW
'''
root = tk.Tk()
root.title(TITLE)
root.attributes('-type', 'dialog')  # makes the window a pop up/dialog


'''
    MAINFRAME AND SUBFRAMES
'''
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky='nwes')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Tree view & File view
# Frame Creation for the folder treeview, file view and the directory entry
f_t_view_frame = ttk.Frame(mainframe)
f_t_view_frame.grid(column=0, row=0)
fn_treeview = FileNavigator(f_t_view_frame)
folder_treeview = TreeNavigator(f_t_view_frame, path=PATH)
dir_entry_frame = DirEntryFrame(f_t_view_frame)

# Notebook
nb = ChangesNotebook(mainframe)

# Extra Information Bar
inf_bar = InfoBar(mainframe)

# Set Padding around the window
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
