from tkinter import StringVar as tkStringVar, BooleanVar as tkBooleanVar


class BaseWidget:
    def __init__(
        self,
        master,
        column=0,
        row=0,
        columnspan=1,
        sticky="",
        brothers: dict = {},
        **kwargs,
    ):
        # Create TTK Frame with parent master
        super().__init__(master, **kwargs)
        # And set Frame on grid
        self.grid(column=column, row=row, columnspan=columnspan, sticky=sticky)

        # Add brothers to the self variables instance
        self.__dict__.update(brothers)

    def tk_init(self):
        raise NotImplementedError

    def bindEntries(self):
        """Default function for binded actions"""
        raise NotImplementedError


class BaseNamingWidget(BaseWidget):
    class Fields:
        def __init__(self, **fields):
            for field in fields:
                # When accessing the var_name return the tk_var
                self.__dict__[field] = fields[field][0]
                # And have var_name.default for the default values
                self.__dict__[field].default = fields[field][1]

        def get_all(self):
            return {
                field: self.__dict__[field].get() for field in self.__dict__
            }

    def bindEntries(self):
        raise NotImplementedError

    def resetWidget(self):
        for field in self.fields.__dict__:
            val = (
                self.fields.__dict__[field].default[0]
                if isinstance(self.fields.__dict__[field].default, tuple)
                else self.fields.__dict__[field].default
            )
            self.fields.__dict__[field].set(val)

    def setCommand(self, var_dict):
        for field in self.fields.__dict__:
            self.fields.__dict__[field].set("")

    @staticmethod
    def appendVarValToDict(dict_: dict = {}):
        raise NotImplementedError
