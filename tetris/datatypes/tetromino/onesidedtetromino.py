from random import randrange
from . import rotation


# Class to describe a unique one-sided tetromino,
# i.e. a tetromino that can be rotated, but not reflected.
class OneSidedTetromino(object):
    def __init__(self, color, data):
        try:
            self.__size = len(data[0])
        except TypeError:
            self.__size = 0

        self.__data = [column_item for row in data for column_item in row]
        self.__color = color

    # __len__ #############################################
    def __len__(self):
        """Gets a number representing the height/width of this tetromino."""
        return self.__size

    # property width_range ################################
    @property
    def width_range(self):
        """A range of columns covering the width/height of this tetromino.
        Mainly for readability."""
        return range(len(self))

    # property height_range ###############################
    height_range = width_range      # only for readability

    # property color ######################################
    @property
    def color(self):
        """Gets the color of this tetromino."""
        return self.__color

    # get_value_at ########################################
    def get_value_at(self, irotation, row, col):
        """Gets the value of a tetromino cell with the given rotation.
        A nonzero value means the space is occupied, otherwise unoccupied."""
        return self.__data[rotation.index(len(self), irotation, row, col)]

    # gen_rows ############################################
    def gen_rows(self, irotation):
        """Generator that iterates through the rows of a
        tetromino with the given rotation."""
        f = self.get_value_at
        for r in self.height_range:
            yield [f(irotation, r, c) for c in self.width_range]

    # gen_rotation ########################################
    def gen_rotation(self, irotation):
        """Generator that iterates through each individual cell of
        a tetromino by first rotating it by the given rotation, then
        moving top-left to bottom-right, yielding tuples of the following
        form:

        (row, col, value at (row,col) with the applied rotation)
        """
        f = self.get_value_at
        for row in self.height_range:
            for col in self.width_range:
                yield (row, col, f(irotation, row, col))

    # create_tetrominoes ##################################
    @classmethod
    def create_tetrominoes(cls):
        """Creates a list of tetrominoes used for the game.
        The item at index zero is the null block, specifically
        designed to run through all block processing code as
        a no-op."""
        return [
            cls((0, 0, 0), [[]]),           # 0: null block

            cls((0, 255, 255), [            # 1: I-shaped block (cyan)
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
            ]),

            cls((0, 255, 0), [              # 2: S-shaped block (green)
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0],
            ]),

            cls((255, 0, 0), [              # 3: Z-shaped block (red)
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ]),

            cls((0, 0, 255), [              # 4: J-shaped block (blue)
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0],
            ]),

            cls((0xFF, 0x99, 0), [          # 5: L-shaped block (orange)
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1],
            ]),

            cls((255, 0, 255), [            # 6: T-shaped block (magenta)
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]),

            cls((255, 255, 0), [            # 7: O-shaped block (yellow)
                [1, 1],
                [1, 1],
            ])
        ]

# Create all tetrominoes now.
tetrominoes = OneSidedTetromino.create_tetrominoes()

# Some utility methods
count = lambda: len(tetrominoes)
get_next = lambda: randrange(1, count())