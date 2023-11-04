class Metadata_ListEntries:
    """
    Draws the Metadata List entries. Inside metadata notebook.
    It has:
        - A Vertical Scrollable Frame with the list of metadata entries
        - A New Tag name entry
        - An Add button to add the new tag
    """

    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=0, row=0, sticky="nsw")

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.field_frame = Vertical_Scrolled_Frame(self.frame)
        self.field_frame.grid(
            column=0, row=0, columnspan=3, pady=3, sticky="nsw"
        )

        self.new_tag_name = tk.StringVar()

        ttk.Label(self.frame, text="New Tag Name").grid(
            column=0,
            row=1,
        )
        self.new_tag_name_entry = ttk.Entry(
            self.frame,
            textvariable=self.new_tag_name,
        )
        self.new_tag_name_entry.grid(column=1, row=1, sticky="w" + "e")

        # Add new tag, button
        self.add_field_button = ttk.Button(
            self.frame, width=5, text="Add", command=self.createMetadataTag
        )
        self.add_field_button.grid(column=2, row=1, sticky="se")

        self.metaDictReset()

        self.metadataEntriesCreate()

    def newTagNameGet(self, *args, **kwargs):
        return self.new_tag_name.get()

    def metaDictTextGet(self, key, *args, **kwargs):
        return self.meta_dict[key].get()

    def metaDictGet(self, *args, **kwargs):
        return self.meta_dict

    def metaDictReset(self, *args, **kwargs):
        self.meta_dict = {
            "title": tk.StringVar(),
            "tracknumber": tk.StringVar(),
            "artist": tk.StringVar(),
            "album": tk.StringVar(),
            "date": tk.StringVar(),
            "genre": tk.StringVar(),
        }

    def getMetadata(self, selection, *args, **kwargs):
        """
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
        """
        self.meta_dict = {
            "title": [],
            "tracknumber": [],
            "artist": [],
            "album": [],
            "date": [],
            "genre": [],
        }
        try:
            for file in selection:
                meta_audio = Meta_Audio(file)

                for meta_item in meta_audio:
                    meta_value = meta_audio.get(meta_item)

                    # Adds to each key the value for this selected item
                    self.meta_dict[meta_item] = (
                        self.meta_dict.get(meta_item, list()) + meta_value
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
            self.metaDictReset()
            return self.meta_dict

    def metaValuesListToStr(self, list_convert, *args, **kwargs):
        """
        Transforms a list into a string separating each value with "; "
        """
        return "; ".join(list_convert)

    def entryFrameReset(self, *args, **kwargs):
        """
        Reset the entry list by deleting all widgets inside
        the entry widget
        """
        for child in self.field_frame.interior.winfo_children():
            child.destroy()

    def metadataSelect(self, *args, **kwargs):
        """
        Resets the frame and repopulates with all the entries and
        their corresponding labels
        """
        selection = fn_treeview.selectedItems()
        self.entryFrameReset()
        self.getMetadata(selection)
        self.metadataEntriesCreate()

    def metadataEntriesCreate(self, *args, **kwargs):
        """Create the metadata list entries with their values"""
        for n, key in enumerate(self.meta_dict):
            ttk.Label(
                self.field_frame.interior, text=key, width=25, anchor="e"
            ).grid(column=0, row=n)

            ttk.Entry(
                self.field_frame.interior,
                width=55,
                textvariable=self.meta_dict[key],
            ).grid(column=1, row=n, sticky="e")

    def createMetadataTag(self, *args, **kwargs):
        """
        Adds a new tag to the metadata tags entries list if the tag
        name is not empty.
        """
        tag_name = self.newTagNameGet()

        if tag_name:
            self.meta_dict[tag_name] = tk.StringVar()
            n = len(self.meta_dict)

            ttk.Label(
                self.field_frame.interior, text=tag_name, width=25, anchor="e"
            ).grid(column=0, row=n)
            ttk.Entry(
                self.field_frame.interior,
                width=55,
                textvariable=self.meta_dict[tag_name],
            ).grid(column=1, row=n, sticky="e")

        else:
            msg = "No name for the new tag. Please type a name"
            inf_bar.lastActionRefresh(msg)
