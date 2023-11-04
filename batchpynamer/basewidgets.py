import tkinter as tk
from tkinter import BooleanVar as tkBooleanVar
from tkinter import StringVar as tkStringVar
from tkinter import ttk

import batchpynamer as bpn


class BaseWidget:
    def __init__(
        self,
        master,
        column=0,
        row=0,
        columnspan=1,
        rowspan=1,
        sticky="nsew",
        **kwargs,
    ):
        # Create TTK Frame with parent master
        super().__init__(master, **kwargs)
        # And set Frame on grid
        self.grid(
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
            sticky=sticky,
        )

    def bindings(self):
        raise NotImplementedError


class BaseFieldsWidget(BaseWidget):
    fields = None

    class Fields:
        def __init__(self, **fields):
            self.__dict__.update(fields)

        def get_all(self):
            return {
                field: self.__dict__[field].get() for field in self.__dict__
            }

        def reset_all(self):
            for field in self.__dict__:
                self.__dict__[field].reset()

    def bindings(self):
        """Defines the binded actions"""
        # Call defocus when combo boxes have items selected
        for var in self.__dict__:
            if isinstance(self.__dict__[var], ttk.Combobox):
                self.__dict__[var].bind("<<ComboboxSelected>>", self.defocus)

    def defocus(self, event=None):
        """
        Clears the highlightning of the comboboxes inside the instance
        whenever any of them changes value.
        """
        for var in self.__dict__:
            if isinstance(self.__dict__[var], ttk.Combobox):
                self.__dict__[var].selection_clear()


class BaseNamingWidget(BaseFieldsWidget):
    def tk_init(self, reset_column_row: tuple = (2, 2)):
        """Creates the reset button"""
        self.reset_button = ttk.Button(
            self,
            width=2,
            text="R",
            command=self.resetWidget,
        )
        self.reset_button.grid(
            column=reset_column_row[0],
            row=reset_column_row[1],
            sticky="se",
            padx=2,
            pady=2,
        )

    def bindings(self):
        super().bindings()

        # Call update new name when each fields are written on
        for field in self.fields.__dict__:
            self.fields.__dict__[field].trace_add(
                "write", bpn.fn_treeview.showNewName
            )

    def resetWidget(self):
        """Resets fields to defined default value"""
        self.fields.reset_all()

    def setCommand(self, var_dict):
        """Sets the proper rename class child fields from the whole dict"""
        for field in self.fields.__dict__:
            self.fields.__dict__[field].set(var_dict[field])

    def appendVarValToDict(dict_={}, *args, **kwargs):
        raise NotImplementedError


class BpnVar:
    def __init__(self, default_val):
        self.default = default_val
        super().__init__(bpn.root, default_val)

    def reset(self):
        self.set(self.default)


class BpnIntVar(BpnVar, tk.IntVar):
    def __init__(self, default_val: int):
        super().__init__(default_val)


class BpnStrVar(BpnVar, tk.StringVar):
    def __init__(self, default_val: str):
        super().__init__(default_val)


class BpnComboVar(BpnStrVar):
    def __init__(self, default_val: tuple):
        self.options = default_val
        super().__init__(default_val[0])


class BpnBoolVar(BpnVar, tk.BooleanVar):
    def __init__(self, default_val: bool):
        super().__init__(default_val)


class VerticalScrolledFrame(ttk.Frame):
    """
    A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand="false")
        canvas = tk.Canvas(
            self,
            bd=0,
            background="gray85",
            highlightthickness=0,
            yscrollcommand=vscrollbar.set,
        )
        canvas.pack(side="left", fill="both", expand="true")
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

        def _on_mousewheel(event):
            """
            Transform the delta event to either 1 or -1
            The mousewheel buttons return an event object with the x and
            y coordinates of the mouse, and in each case:
            The mousewheel a delta with the value of the overall position
            of the mousewheel.
            The button-4/5 a num with which button was pressed.
            """

            def delta(event):
                """
                When the event.num is 5 (down) or delta is negative value
                return a 1, else return -1
                """
                if event.num == 5 or event.delta < 0:
                    return 1
                return -1

            # Get the direction of the scroll and apply it
            direction = delta(event)
            canvas.yview_scroll(direction, "units")

        def _bound_to_mousewheel(event):
            """
            What to bind to the mousewheel
            The <MouseWheel> event is for windows
            While the <Button-4/5> is for linux
            """
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            """Unbind the mouswheel"""
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        def _binds():
            """
            Only bind the mousewheel when over the widget and unbind when
            not over it
            """
            canvas.bind("<Enter>", _bound_to_mousewheel)
            canvas.bind("<Leave>", _unbound_to_mousewheel)

        _binds()


class PopUpWindow(tk.Toplevel):
    def __init__(self, title=""):
        # Pop Up windows always are children of root
        super().__init__(bpn.root, bg="gray85")
        self.title(title)
        self.attributes("-type", "dialog")


class ErrorFrame(PopUpWindow):
    """Error frame with an error message and an "Okay" button"""

    def __init__(self, error_desc="Non-descript"):
        # Create a new window
        super().__init__(title="ERROR")

        # Label with error description
        ttk.Label(self, text=f"ERROR: {error_desc}").grid(
            column=0, row=0, padx=5, pady=5
        )

        # Okay button destroys the window
        ttk.Button(self, text="Okay", command=self.destroy).grid(
            column=0, row=1, padx=5, pady=5
        )
