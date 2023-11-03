class Filters_Widget(basewidgets.BaseWidget, ttk.LabelFrame):
    """
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
    """

    def __init__(self, master, *args, **kwargs):
        self.lf = ttk.Labelframe(master, text="Filter File View")
        self.lf.grid(column=0, row=0, sticky="w")

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
        ttk.Label(self.lf, text="Mask").grid(column=0, row=0, sticky="e")
        self.mask_entry = ttk.Entry(self.lf, width=10, textvariable=self.mask)
        self.mask_entry.grid(column=1, row=0, sticky="w")

        # Extension list, entry
        ttk.Label(self.lf, text="Ext(s)").grid(column=0, row=1, sticky="e")
        self.ext_entry = ttk.Entry(self.lf, width=10, textvariable=self.ext)
        self.ext_entry.grid(column=1, row=1, sticky="w")

        # Folders, checkbutton
        self.folders_check = ttk.Checkbutton(
            self.lf,
            text="Folders",
            variable=self.folders,
        )
        self.folders_check.grid(column=2, row=0, sticky="w")

        # Files, checkbutton
        self.files_check = ttk.Checkbutton(
            self.lf,
            text="Files",
            variable=self.files,
        )
        self.files_check.grid(column=2, row=1, sticky="w")

        # Hidden files, checkbutton
        self.hidden_check = ttk.Checkbutton(
            self.lf,
            text="Hidden",
            variable=self.hidden,
        )
        self.hidden_check.grid(column=3, row=0, sticky="w")

        # Reverse files, checkbutton
        self.reverse_check = ttk.Checkbutton(
            self.lf,
            text="Reverse",
            variable=self.reverse,
        )
        self.reverse_check.grid(column=3, row=1, sticky="w")

        # Files before directories, checkbutton
        self.files_before_dirs_check = ttk.Checkbutton(
            self.lf,
            text="Files before Dirs",
            variable=self.files_before_dirs,
        )
        self.files_before_dirs_check.grid(
            column=4, row=1, columnspan=2, sticky="w"
        )

        # Recursive depth levels, spinbox
        ttk.Label(self.lf, text="Recursive Levels").grid(
            column=4, row=0, sticky="ew"
        )
        self.depth_spin = ttk.Spinbox(
            self.lf,
            width=3,
            from_=-1,
            to=MAX_NAME_LEN,
            textvariable=self.depth,
        )
        self.depth_spin.grid(column=5, row=0)

        # Name lenght group
        ttk.Label(self.lf, text="Name lenght").grid(
            column=6, row=0, columnspan=4
        )

        # Minimum name lenght, spinbox
        ttk.Label(self.lf, text="min").grid(column=6, row=1, sticky="e")
        self.name_len_min_spin = ttk.Spinbox(
            self.lf, width=3, to=MAX_NAME_LEN, textvariable=self.min_len
        )
        self.name_len_min_spin.grid(column=7, row=1, sticky="w")

        # Maximum name lenght, spinbox
        ttk.Label(self.lf, text="max").grid(column=8, row=1, sticky="e")
        self.name_len_max_spin = ttk.Spinbox(
            self.lf, width=3, to=MAX_NAME_LEN, textvariable=self.max_len
        )
        self.name_len_max_spin.grid(column=9, row=1, sticky="w")

        # Reset, button
        self.reset_button = ttk.Button(
            self.lf, width=2, text="R", command=self.resetWidget
        )
        self.reset_button.grid(column=10, row=1, sticky="nw", padx=2, pady=2)

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
        """Defines the binded actions"""
        self.mask_entry.bind("<FocusOut>", fn_treeview.refreshView)
        self.mask_entry.bind("<Return>", fn_treeview.refreshView)
        self.ext_entry.bind("<FocusOut>", fn_treeview.refreshView)
        self.ext_entry.bind("<Return>", fn_treeview.refreshView)
        self.folders.trace_add("write", fn_treeview.refreshView)
        self.files.trace_add("write", fn_treeview.refreshView)
        self.hidden.trace_add("write", fn_treeview.refreshView)
        self.hidden.trace_add("write", folder_treeview.refreshView)
        self.files_before_dirs.trace_add("write", fn_treeview.refreshView)
        self.reverse.trace_add("write", fn_treeview.refreshView)
        self.min_len.trace_add("write", fn_treeview.refreshView)
        self.max_len.trace_add("write", fn_treeview.refreshView)
        self.depth.trace_add("write", fn_treeview.refreshView)

    def resetWidget(self, *args, **kwargs):
        self.mask.set("")
        self.ext.set("")
        self.folders.set(True)
        self.files.set(True)
        self.hidden.set(False)
        self.files_before_dirs.set(False)
        self.reverse.set(False)
        self.min_len.set(0)
        self.max_len.set(MAX_NAME_LEN)
        self.depth.set(0)
