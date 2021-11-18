import sys
import random
import pygame

from datatypes import event
from datatypes import EmptyObject

from tetris.datatypes import tetrisgrid
from tetris.datatypes import tetromino

# _game_loop ##############################################
def _game_loop(screen, config):

    # Do not enter loop if no screen is provided.
    if not screen:
        print("Screen not provided.  No need to enter game loop.")
        return 1

    # We'll be using this to keep track of the game state.
    state = EmptyObject(
        delay=50,
        running=True,
        paused=False,
        game_over=False,

        player=EmptyObject(score=0, block_count=0, line_count=0),
        next_level_lines=config.LINES_PER_LEVEL,

        next_frame_draw_only=0,

        gravity_event=event.CyclicCounter(
            limit=config.GRAVITY_FRAME_DELAY_START,
        ),

        playing_field=tetrisgrid.TetrisGrid(config.BOARD_SIZE),

        block=EmptyObject(
            current_index=0,
            next_index=0,
            pos=tetromino.Position(),
            next_pos=tetromino.Position(),
        ),

        # Actions to be performed.  We will not send raw input
        # events to the game logic.  Instead, a function that
        # handles the raw input will translate it into actions
        # that the player is trying to attempt, which will then
        # be handled by the game logic instead.
        action=EmptyObject(
            rotate=EmptyObject(
                cw=False,
                ccw=False,
            ),
            move=EmptyObject(
                left=False,
                right=False,
                down=False,
            ),
        ),

        current_rows_cleared=[],

        color=EmptyObject(),
    )

    # A function to get a block index.
    state.block.next_index = tetromino.get_next()

    # A function for choosing colors in a line clear effect.
    def line_clear(grid, row, col, low=50, high=256):

        # I'm using separately named variables
        # in case I want to change something.
        #
        # For now, I'm fine with a greyscale effect.
        #
        rr = lambda: random.randrange(low, high)
        r = rr()
        g = r
        b = r
        return (r, g, b)
    state.color.line_clear = line_clear

    # A function for choosing colors in a game over effect.
    def game_over(grid, row, col, low=50, high=250):
        rr = lambda: random.randrange(low, high)
        r = rr()
        g = rr()
        b = rr()
        return (r, g, b)
    state.color.game_over = game_over

    # Load modules needed to run the game...
    from tetris import framestate
    from tetris import gameinput
    from tetris import gamelogic
    from tetris import gameoutput

    # Let's get this party started!
    while state.running:
        with framestate.frame(state, delay_func=pygame.time.delay):
            if gameinput.process_input_and_events(state):
                gamelogic.game_logic(state, config, screen)
                gameoutput.draw_frame(state, config, screen)

    print(f"You cleared {state.player.line_count} line(s).")
    print(f"You placed  {state.player.block_count} block(s).")

    return state.player.score


# main #############################################
def main():
    """Entry point."""

    # Game configuration.
    config = EmptyObject(
        SCREEN_SIZE=(640, 480),         # Screen size in pixels
        BOARD_SIZE=(12, 20),            # Board size in cells
        CELL_SIZE=(20, 20),             # Cell size in pixels

        SCREEN_COLOR=(0, 0, 0),         # Background color for screen
        GRID_COLOR=(25,) * 3,           # Color of inner grid lines
        GRID_BORDER_COLOR=(255,) * 3,   # Color of grid border

        GRID_XY=(20, 20),               # Pixel position of grid

        scoring=EmptyObject(
            DROP_BLOCK=25,
            TETRIS_BONUS=200,
        ),

        LINES_PER_LEVEL=3,

        LINE_CLEAR_FRAME_DELAY=5,

        GRAVITY_FRAME_DELAY_START=25,
    )

    # Scoring for when a line is cleared.
    #
    # 25 points   -> placing a block without clearing a line
    #                or causing a game over
    # 100 points  -> clearing 1 line
    # 200 points  -> clearing 2 lines
    # 400 points  -> clearing 3 lines
    # 1000 points -> clearing 4 lines
    #
    config.scoring.CLEAR_LINE = lambda lines, scoring=config.scoring: \
        (scoring.DROP_BLOCK << (1 + lines)) \
            + (lines >= 4) * scoring.TETRIS_BONUS


    # Separate sizes and positions into individual components.
    config.SCREEN_WIDTH, config.SCREEN_HEIGHT = config.SCREEN_SIZE
    config.BOARD_WIDTH, config.BOARD_HEIGHT = config.BOARD_SIZE
    config.GRID_X, config.GRID_Y = config.GRID_XY
    config.CELL_WIDTH, config.CELL_HEIGHT = config.CELL_SIZE

    # Run the game.
    try:
        pygame.init()

        screen = pygame.display.set_mode(config.SCREEN_SIZE)
        pygame.display.set_caption("pygame Tetris")

        score = _game_loop(screen, config)
    finally:
        pygame.quit()

    print(f"Your score was: {score}")

    return -score if score < 0 else 0


# Do not run if this is being included as a script.
if __name__ == "__main__":
    sys.exit(main())