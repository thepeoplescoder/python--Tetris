# Imports
import pygame
from datatypes import EmptyObject
from tetris.datatypes import tetromino

# draw_frame #######################################
def draw_frame(state, config, screen):
    """The function responsible for drawing the entire
    frame.  All drawing starts here."""
    screen.fill(config.SCREEN_COLOR)                # Clear the screen.
    rect = _draw_board(state, config, screen)       # Draw the board.
    _show_next_block(state, config, screen, rect)   # Show the next block.
    pygame.display.flip()                           # Make it all visible.

# _draw_board #############################################
def _draw_board(state, config, screen):

    # Select the block to display.  If we are in a game over
    # state, this chooses the null block, which displays nothing.
    position = state.block.pos
    tetro = tetromino.tetrominoes[
        int(not state.game_over) and state.block.current_index
    ]

    # Draw the grid representing the game board,
    # and return a rectangle bounding the modified
    # pixels.
    return _draw_grid_at(
        state.playing_field, config,
        screen, config.GRID_XY, config.CELL_SIZE,
        position, tetro
    )

# _show_next_block #################################
def _show_next_block():
    """Shows the next block the user will have to manipulate."""
    from tetris.datatypes import tetrisgrid
    from random import randrange

    next_block_grid = tetrisgrid.TetrisGrid(6, 6)
    pos = [
        [0, 0, 0],              # null
        [1, 1, 0],              # I
        [2, 2, 0],              # S
        [2, 2, 0],              # Z
        [2, 2, 0],              # J
        [1, 1, 0],              # L
        [1, 1, 0],              # T
        [2, 2, 0],              # O
    ]

    effects = EmptyObject(
        rotator=EmptyObject(
            rotation=0,
            counter=0,
            update_at=20,
        ),
        game_over=EmptyObject(
            need_to_do=True
        ),
    )

    def game_over_color(row, col, low=50, high=256):
        rgb = randrange(low, high)
        return (rgb, 0, rgb)

    # The function that does the actual work.
    def _show_next_block(state, config, screen, board_rect):
        """Shows the next block the user will have to manipulate."""
        rect_next_block = board_rect.copy()
        rect_next_block.width = next_block_grid.width * config.CELL_WIDTH
        rect_next_block.height = next_block_grid.height * config.CELL_HEIGHT
        rect_next_block.centery = board_rect.centery
        rect_next_block.x += board_rect.width + (2 * config.CELL_WIDTH)

        if state.game_over:
            index = 0
            if effects.game_over.need_to_do:
                for row in range(next_block_grid.height):
                    row = next_block_grid[row]
                    row[:] = [game_over_color] * len(row)
                effects.game_over.need_to_do = False
        else:
            index = state.block.next_index
            effects.rotator.counter += 1
            if effects.rotator.counter >= effects.rotator.update_at:
                effects.rotator.counter -= effects.rotator.update_at
                effects.rotator.rotation += 1
            pos[index][2] = effects.rotator.rotation

        _draw_grid_at(
            next_block_grid, config,
            screen, rect_next_block.topleft, config.CELL_SIZE,
            pos[index], tetromino.tetrominoes[index],
        )

    # We want the inner function.
    return _show_next_block
_show_next_block = _show_next_block()

# _cell_to_pixel ##########################################
def _cell_to_pixel(cell_position, cell_size_in_pixels, pixel_position):
    row, col = cell_position
    width, height = cell_size_in_pixels
    x0, y0 = pixel_position
    return (x0 + col * width, y0 + row * height)

# _draw_grid_at ###########################################
def _draw_grid_at():

    # Callback functions.
    def draw_grid_cell(grid, cell, obj):
        row, col, color = cell
        rect = obj.rect_cell
        rect.topleft = _cell_to_pixel((row, col), rect.size, obj.xy0)
        obj.rect_grid.union_ip(pygame.draw.rect(obj.surface, color, rect))
        return obj
    def draw_grid_line(grid, line, obj):
        xy0 = _cell_to_pixel(line[0], obj.rect_cell.size, obj.xy0)
        xy1 = _cell_to_pixel(line[1], obj.rect_cell.size, obj.xy0)
        pygame.draw.line(obj.surface, obj.line_color, xy0, xy1)
        return obj
    def draw_grid_border(grid, obj):
        obj.rect_grid.inflate_ip(2, 2)
        pygame.draw.rect(obj.surface, obj.border_color, obj.rect_grid, 1)
        return obj

    # This is the actual function that will get called.
    def _draw_grid_at(grid, config,
                surface, xy, cell_size,
                position, tetro
        ):
        """Draws the playing field, i.e. the board on which
        the game is played.

        Returns a pygame.Rect object describing the area
        modified by this function."""

        # To assist in drawing.
        rect_modified = pygame.Rect(xy, cell_size)

        # Now that we have everything we need, we can draw the board.
        return grid.draw_with_piece(
            position, tetro,

            default_cell_value=config.SCREEN_COLOR,

            draw_cell=draw_grid_cell,
            draw_line=draw_grid_line,
            draw_border=draw_grid_border,

            initial_object=EmptyObject(
                surface=surface,
                xy0=xy,
                rect_grid=rect_modified,
                rect_cell=rect_modified.copy(),
                line_color=config.GRID_COLOR,
                border_color=config.GRID_BORDER_COLOR,
            )
        ).rect_grid

    # Return the reference to the function.
    return _draw_grid_at
_draw_grid_at = _draw_grid_at()