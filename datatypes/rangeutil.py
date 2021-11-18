RangeType = type(range(0))

# slice_to_range ##########################################
def slice_to_range(sl):
    if isinstance(sl, RangeType):       # Leave ranges alone.
        return sl
    try:
        return range(
            sl.start if sl.start else 0,
            sl.stop,
            sl.step if sl.step else 1,
        )
    except:
        return None

# range_to_slice ##########################################
def range_to_slice(ra):
    if isinstance(ra, slice):               # Leave slices alone.
        return ra
    try:
        return slice(ra.start, ra.stop, ra.step)
    except:
        return None

# issubrange ##############################################
def issubrange(r, super_range):
    """Checks to see if r is contained in super_range.
    Works on integers, ranges, and slices."""

    # If the "range" is an integer, then this is
    # an easy check.
    if isinstance(r, int):
        if isinstance(super_range, int):
            return 0 <= r < super_range
        else:
            return r in slice_to_range(super_range)

    # Otherwise, do the conversions and continue.
    r = slice_to_range(r)
    super_range = slice_to_range(super_range)

    # The empty range is a subrange of everything.
    if not r:
        return True

    # The empty range cannot be a superrange of anything.
    if not super_range:
        return False

    # Are we out of our range?
    if r.start not in super_range:      # First value in r
        return False
    elif r[-1] not in super_range:      # Last value in r
        return False

    # Does our assumed subrange step on the same values
    # as the given superrange?  i.e. is the step of r
    # a multiple of the step of super_range?  If so, then
    # we've passed all of the tests.
    return (r.step % super_range.step) == 0