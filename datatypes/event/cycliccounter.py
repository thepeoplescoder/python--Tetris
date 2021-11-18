import numbers

# class CyclicCounter #####################################
class CyclicCounter(object):
    """Class to keep track of counting items in a cyclic fashion.
    Includes a poll() method which returns True if the counting limit
    has been passed or reached.  This can be used for minor event
    handling, such as ensuring something only takes place every 20
    times, for example."""

    # __init__ ############################################
    def __init__():

        # Necessary constants for constructor.
        NUMERIC_KWARGS = {
            "start_at": 0,
            "limit": 1,
        }

        # This is the actual constructor.
        def __init__(self, **kwargs):
            """Creates a counter with a given limit and starting point.
            The internal counter cannot be changed directly once set.

            Keyword arguments:
               start_at -> initial value of the internal counter
               limit    -> the limit at which the counter should reset.

            Note that when the limit is surpassed, the internal counter
            is subtracted by the amount of limit instead of simply being
            reset to zero."""

            # Ensure required arguments are numeric.
            for key, vdefault in NUMERIC_KWARGS.items():
                if not isinstance(kwargs.get(key, vdefault), numbers.Real):
                    raise TypeError("Expected %s to be numeric" % (key,))

            # Get arguments.
            start_at = kwargs.pop("start_at", NUMERIC_KWARGS["start_at"])
            limit = kwargs.pop("limit", NUMERIC_KWARGS["limit"])

            # Ensure no leftovers.
            if kwargs:
                key, _ = kwargs.popitem()
                raise TypeError("{0}: Invalid argument: {1}" \
                    .format(__class__, key))

            # Okay, now we can initialize this object.
            self.__count = start_at
            self.limit = limit      # Use the property to set this value.
        return __init__
    __init__ = __init__()

    # property limit (getter) #############################
    @property
    def limit(self):
        """Retrieves the currently set limit."""
        return self.__limit

    # property limit (setter) #############################
    @limit.setter
    def limit(self, value):
        """Sets the limit, which must be a positive integer."""
        self.__limit = int(max(value, 1))

    # property limit_reached (getter) #####################
    @property
    def limit_reached(self):
        """Checks if the limit has been reached and returns True or False
        based on that information.

        Note: If this function returns True, the internal counter will be
        reset, and subsequent usage of this property will return False until
        the internal counter surpasses the limit again."""
        if self.__count < self.__limit:
            return False
        else:
            self.__count -= self.__limit
            return True

    # poll ################################################    
    def poll(self, delta=1):
        """Updates the internal state of the object and checks to
        see if the limit was reached in doing so."""
        self.__count += int(0 + delta)  # Raise error if not numeric
        return self.limit_reached