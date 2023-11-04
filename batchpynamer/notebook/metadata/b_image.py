class Metadata_Img:
    """
    Draws the Metadata Image widget. Inside metadata notebook.
    It has:
        - An entry to write the path to the new image
        - A X button to empty the new image entry
        - A canvas to display the metadata image
    """

    def __init__(self, master, *args, **kwargs):
        self.frame = ttk.Frame(master)
        self.frame.grid(column=1, row=0, sticky="ns")

        # Empty photo image to force the label to use pixel size
        self.photo_image = tk.PhotoImage()

        self.picture = None
        self.image_path = tk.StringVar()

        # Path to new image, entry
        self.image_path_entry = ttk.Entry(
            self.frame, textvariable=self.image_path
        )
        self.image_path_entry.grid(column=0, row=0, sticky="ew")

        self.reset_path_button = ttk.Button(
            self.frame, width=2, text="X", command=self.resetPath
        )
        self.reset_path_button.grid(column=1, row=0, sticky="w")

        # Image frame, Label
        self.img = tk.Label(
            self.frame,
            relief="sunken",
            background="gray10",
            image=self.photo_image,
            height=250,
            width=250,
        )
        self.img.grid(column=0, row=1)

        # Image size, label
        self.size_label = ttk.Label(self.frame, text="No Image")
        self.size_label.grid(column=0, row=2)

    def imageGet(self, *args, **kwargs):
        return self.picture

    def imagePathGet(self, *args, **kwargs):
        return self.image_path.get()

    def resetPath(self, *args, **kwargs):
        self.image_path.set("")

    def imageLoad(self, *args, **kwargs):
        """
        Loads the first image binded to the selected files and checks if
        they are all the same. If not then it loads no image.
        Also does nothing if the file doesnt have an image attached.
        """
        # Error handling if theres no image
        try:
            selection = fn_treeview.selectedItems()

            # Load the first image, and well use it to compare against
            self.picture = Meta_Picture(selection[0])

            # If the selected file isnt valid
            if self.picture == "not valid":
                # set the size label to show such message
                self.size_label.config(text="Not a valid file")
                self.picture = None

            # Else if checks against that first loaded image every other image
            # When it finds a diferent image breaks out of the loop and
            # executes the if
            elif not all(
                Meta_Picture(file) == self.picture for file in selection
            ):
                self.size_label.config(text="Different images")
                self.picture = None

        except (IndexError, AttributeError):
            # Set the size label to show theres no image
            self.size_label.config(text="No image")

    def imageShow(self, *args, **kwargs):
        """Shows the first image binded to the files"""
        self.picture = None
        self.imageLoad()
        if self.picture is not None:
            im = PIL.Image.open(BytesIO(self.picture))
            # Get image size before resizing
            im_width, im_height = map(str, im.size)

            # Resize
            # im = im.resize((250, 250), PIL.Image.ANTIALIAS)
            im = im.resize((250, 250), PIL.Image.LANCZOS)

            # Show image
            render = PIL.ImageTk.PhotoImage(im)
            self.img.image = render
            self.img.config(image=render)

            # Show image size
            size_text = "{} x {}".format(im_width, im_height)
            self.size_label.config(text=size_text)

        else:
            self.img.config(image=self.photo_image)
