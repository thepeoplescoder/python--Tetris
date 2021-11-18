from datatypes import grid
from tetris.datatypes import tetromino

# TetrisGrid ##############################################
class TetrisGrid(grid.Base):

    # gen_block_overlay ###################################
    def gen_block_overlay(self, pos, tetro):

        # Unpack arguments.
        pos = tetromino.Position.cast(pos)
        row = pos.row
        col = pos.column
        rotation = pos.rotation

        # Other initializations
        occupy_this_cell = tetro.color
        iterator_block_row = None

        # Iterate through every row in our playing field.
        for row_index, board_row in enumerate(self):
            board_row = list(board_row)     # intentionally make a copy

            # If we're in a row where our block is to be placed...
            if row <= row_index < row + len(tetro):

                # Get the block's row generator if we don't have it.
                # To enable positioning tetrominoes *above* the grid,
                # we will skip the rows that we can't see.
                if not iterator_block_row:
                    iterator_block_row = tetro.gen_rows(rotation)
                    for skip_index in range(row, 0):
                        next(iterator_block_row)

                # What does the current row on this tetromino look like?
                # Superimpose it onto our grid.
                for dcol, is_solid in enumerate(next(iterator_block_row)):
                    if is_solid:
                        board_row[col + dcol] = occupy_this_cell

            # Return the row, either as-is, or a modified copy.
            yield board_row

    # is_valid_move #######################################
    def is_valid_move(self, pos, tetro):
        """Checks to see if the given tetromino with the given
        rotation can be placed on the board with the given position."""
        pos = tetromino.Position.cast(pos)

        # Leave if any collisions are detected whatsoever.
        for drow, dcol, is_solid in tetro.gen_rotation(pos.rotation):
            if is_solid and self[pos.row + drow][pos.column + dcol]:
                return False

        # No collisions detected.  This move is valid.
        return True

    # place_piece_nocheck #################################
    def place_piece_nocheck(self, pos, tetro):
        """Places a piece onto the board without bounds checking."""
        pos = tetromino.Position.cast(pos)
        grid = self.raw_grid
        for drow, dcol, is_solid in tetro.gen_rotation(pos.rotation):
            if is_solid:
                grid[pos.row + drow][pos.column + dcol] = tetro.color

    # draw_with_piece #####################################
    def draw_with_piece(self, pos, tetro, **kwargs):
        """Draws the grid with the given piece at the specified position.
        All drawing is handled via user-defined callbacks in the form of:

            obj1 = callback(this_grid, description, obj0)

        If the callback receives a description of the thing to be drawn;
        lines and cells in this case.

        If the callback does not need a description of the thing to be drawn,
        in this case, the border, then the following form is used:

            obj1 = callback(this_grid, obj0)
        """

        # Extract appropriate keyword argument values.
        draw_cell = kwargs["draw_cell"]
        draw_line = kwargs["draw_line"]
        draw_border = kwargs["draw_border"]
        obj = kwargs["initial_object"]
        default_cell_value = kwargs["default_cell_value"]

        # Draw the cells.
        if callable(draw_cell):
            for row, board_row in enumerate(    # Each row from playing field
                        self.gen_block_overlay(pos, tetro)
                    ):
                for col, cell_value in enumerate(board_row):
                    if callable(cell_value):    # 
                        cell_value = cell_value(self, row, col)
                    if cell_value is None:      # Supply default
                        cell_value = default_cell_value
                    obj = draw_cell(self, (row, col, cell_value), obj)

        # Vertical and horizontal lines.
        if callable(draw_line):
            for col in range(self.width):
                obj = draw_line(self, ((0, col), (self.height, col)), obj)
            for row in range(self.height):
                obj = draw_line(self, ((row, 0), (row, self.width)), obj)

        # Draw the border.
        if callable(draw_border):
            obj = draw_border(self, obj)

        # Return the transformed object.
        return obj

    # clear_row ###########################################
    def clear_row(self, *rows):
        """Clears the given rows in place, moves the rows above
        down, and replaces the cleared rows with empty rows on top."""

        # Essentially remove the references to
        # the given rows.  Setting them to None
        # is sufficient as each row must point to
        # a valid list.
        for row in rows:
            self.raw_grid[row] = None

        # Remove the marked row, and add
        # a brand new row to the top.
        for row in rows:
            self.raw_grid.remove(None)
            self._insert_empty_row(0)