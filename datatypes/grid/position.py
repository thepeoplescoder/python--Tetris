import datatypes.castable

# class Position ##########################################
class Position(datatypes.castable.Castable):
    """Identifies a location of a cell on a grid object."""

    # __init__ ############################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row = kwargs.pop("row", 0)         # Remove args as
        self.column = kwargs.pop("column", 0)   # they are consumed.

    # __repr__ ############################################
    def __repr__(self):
        return "<grid.Position(%d, %d) at %x>" % (self.row,
            self.column, id(self))

    # cast ################################################
    @classmethod
    def cast(cls, *args, **kwargs):
        """Typecasting for grid.Position datatypes."""

        # First argument is the object to convert and is required.
        obj = args[0]

        # Set up constructor arguments for types that aren't ours.
        if not isinstance(obj, cls):
            if isinstance(obj, (tuple, list)):  # tuples and lists
                kwargs["row"] = obj[0]
                kwargs["column"] = obj[1]
            else:                               # anything with a row
                if hasattr(obj, "row"):         # or column attribute
                    kwargs["row"] = obj.row
                if hasattr(obj, "column"):
                    kwargs["column"] = obj.column

            # The cast is invalid if we couldn't extract information.
            if "row" not in kwargs and "column" not in kwargs:
                raise TypeError("Invalid cast")

        # Fall through to parent behavior:
        #    * If the first positional argument is an instance of
        #      our class, then return the first positional argument.
        #    * Otherwise, send the keyword arguments to the appropriate
        #      constructor.
        return super().cast(*args, **kwargs)