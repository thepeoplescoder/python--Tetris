# class Castable ##########################################
class Castable(object):
    """Class to describe an object that supports typecasting behavior."""

    # __init__ ############################################
    def __init__(self, *args, **kwargs):
        """Does nothing.  Included for completeness."""
        pass

    # cast ################################################
    @classmethod
    def cast(cls, *args, **kwargs):
        """Default behavior for explicit type conversion.

        The first argument is the object to be converted, and
        is required.  Each subsequent positional argument is
        passed to the constructor of the type we are converting
        to."""

        # If we recognize the required first argument as one
        # of our own, then return it.  We don't need to make
        # an equivalent object of this type.
        if isinstance(args[0], cls):
            return args[0]

        # Otherwise if all else fails, send the keyword
        # arguments to the appropriate constructor.
        return cls(*args[1:], **kwargs)