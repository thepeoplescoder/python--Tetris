# initialization/deinitialization of a frame.

# Imports
import contextlib

from datatypes import EmptyObject
from tetris.datatypes import tetromino

# start ###################################################
@contextlib.contextmanager
def frame(state, delay_func):
    """Setup/teardown of the current frame."""

    # Delay for a little bit.
    if callable(delay_func):
        delay_func(state.delay)

    # If we're doing more than just drawing...
    if state.next_frame_draw_only < 1:

        # Aliases
        block = state.block
        pos = block.pos
        playing_field = state.playing_field

        # If we have any lines to clear from the previous frame,
        # clear them now so it will be reflected in this frame.
        # This code essentially does nothing if there are no lines
        # to clear.
        playing_field.clear_row(*state.current_rows_cleared)
        state.current_rows_cleared.clear()

        # If we don't have a current block, then get it from
        # the next block.  If the new block to be placed cannot
        # fit, then the game over state is set.
        if not (block.current_index or state.game_over):
            block.current_index = block.next_index
            block.next_index = tetromino.get_next()

            tetro = tetromino.tetrominoes[block.current_index]

            pos.row = 0
            pos.column = playing_field.width    # Here, we are
            pos.column -= len(tetro)            # simply centering
            pos.column = int(pos.column / 2)    # the block.
            pos.rotation = 0

            # It's game over if it doesn't fit.  Prepare a visual
            # representation of that concept.
            state.game_over = not playing_field.is_valid_move(pos, tetro)
            if state.game_over:
                playing_field.place_piece_nocheck(pos, tetro)

        # The block's next position will be based on its current position.
        EmptyObject.field_copy(block.next_pos, pos)

    # Return how many frames remain where we will only draw.
    try:
        yield state.next_frame_draw_only

    # If we're only drawing, decrease the frame count.
    finally:
        if state.next_frame_draw_only > 0:
            state.next_frame_draw_only -= 1
        elif state.next_frame_draw_only < 0:    # This should never be
            state.next_frame_draw_only = 0      # a negative number.