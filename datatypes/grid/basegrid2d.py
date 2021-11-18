from . import position
from datatypes.rangeutil import issubrange

class BaseGrid2D(object):

    # We need something to define the behavior of a row.
    class _Row(object):
        INVALID_CELL = object()     # Use a unique dummy object for this

        def __len__(self):                      # number of columns
            return len(self.raw_row)

        def __getitem__(self, index):           # replaces get_cell_at()
            if issubrange(index, len(self)):
                return self.raw_row[index]
            else:
                return self.INVALID_CELL
        def __setitem__(self, index, value):    # row manipulation with
            if self.__grid:                     # fallthrough bounds checking
                if issubrange(index, len(self)):
                    if value is not self.INVALID_CELL:
                        if value is not self.__grid.INVALID_ROW:
                            self.raw_row[index] = value

        def __iter__(self):                     # iterate through every
            return iter(self.raw_row)           # column

        def __init__(self, grid, row):          # Constructor
            self.__grid = grid
            self.__row = row

        @property
        def raw_row(self):                      # Use at own risk
            g = self.__grid
            if g:
                return g.raw_grid[self.__row]
            else:
                return tuple()

        @property                       # number of columns
        def width(self):                # (for readability)
            return len(self)


    # Invalid positions to be reported by methods.
    # A cell must never contain these values.
    INVALID_CELL = _Row.INVALID_CELL
    INVALID_ROW = _Row(None, 0)

    # make_raw_empty_row ##################################
    @staticmethod
    def make_raw_empty_row(width):
        return [None] * width   # This is how we will define an empty row.

    # make_raw_empty_grid #################################
    @classmethod
    def make_raw_empty_grid(cls, *size):
        if len(size) == 1:
            size = size[0]

        width, height = size

        if width < 1 or height < 1:
            raise TypeError("Width and height must be positive numbers")

        s = []
        for count in range(height):
            s.append(cls.make_raw_empty_row(width))

        return s

    # __init__ ############################################
    def __init__(self, *size):
        """Constructor.  This simply sets every cell on the
        grid to None, which means that the cell is empty and
        is therefore traversible."""
        self.raw_grid = self.make_raw_empty_grid(*size)

    # is_valid ############################################
    def is_valid(self):
        """Sanity check to make sure the object wasn't corrupted."""
        for row in self:
            if len(row) != self.width:
                return False
            elif self.INVALID_CELL in row:
                return False
            elif self.INVALID_ROW in row:
                return False
        return True

    # property width ######################################
    @property
    def width(self):
        return len(self.raw_grid[0])

    # property height #####################################
    @property
    def height(self):
        return len(self)

    # property size #######################################
    @property
    def size(self):
        return (self.width, self.height)

    # __iter__ ############################################
    def __iter__(self):
        return iter(self.raw_grid)

    # __len__ #############################################
    def __len__(self):
        return len(self.raw_grid)

    # __getitem__ #########################################
    def __getitem__(self, row):
        """Retrieves a row from the grid with bounds checking.
        Replaces get_row_at()."""
        if isinstance(row, slice):
            raise TypeError("Slicing on grid rows not allowed.")
        elif issubrange(row, len(self)):
            return self._Row(self, row)
        else:
            return self.INVALID_ROW

    # _insert_empty_row ###################################
    def _insert_empty_row(self, index):
        self.raw_grid.insert(index, [None] * self.width)
