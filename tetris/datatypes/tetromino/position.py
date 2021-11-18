from datatypes import grid

# tetromino.position.Position #############################
class Position(grid.Position):

    # __init__ ############################################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rotation = kwargs.pop("rotation", 0)   # Remove args as they
                                                    # are consumed.

    # __repr__ ############################################
    def __repr__(self):
        return "<tetromino.Position(%d, %d, %d) at %x>" % (self.row,
            self.column, self.rotation, id(self))

    # cast ################################################
    @classmethod
    def cast(cls, *args, **kwargs):

        # The first argument is the object to convert and is required.
        obj = args[0]

        # Handle types that we can convert
        if not isinstance(obj, cls):
            if isinstance(obj, (tuple, list)):      # tuples and lists
                kwargs["rotation"] = obj[2]
            elif hasattr(obj, "rotation"):          # anything with a
                kwargs["rotation"] = obj.rotation   # rotation attribute

            # tetromino.position.Position objects can be upcasted
            # from regular grid.Position objects, as the rotation
            # field will default to zero.

        # Fall through to parent behavior.
        return super().cast(*args, **kwargs)