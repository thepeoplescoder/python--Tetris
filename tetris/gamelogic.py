from datatypes import EmptyObject
from tetris.datatypes import tetromino

def _game_over_effect():
    counter = 0
    done = False
    def game_over_effect(state):
        nonlocal counter, done
        if done:
            return
        playing_field = state.playing_field
        if counter < playing_field.height:
            row = (playing_field.height - 1) - counter
            row = playing_field[row]
            row[:] = [state.color.game_over] * len(row)
            counter += 1
        else:
            done = True
    return game_over_effect
_game_over_effect = _game_over_effect()

# game_logic ##############################################
def game_logic(state, config, screen):
    """Primary function that handles the game logic."""

    # There's no point in handling the game logic
    # or if we are only doing drawing for this frame.
    if state.next_frame_draw_only or state.paused:
        return

    # Aliases
    block = state.block
    pos = block.pos
    next_pos = block.next_pos
    action = state.action

    playing_field = state.playing_field
    is_valid_move = playing_field.is_valid_move

    gravity_event = state.gravity_event

    # Current block
    tetro = tetromino.tetrominoes[block.current_index]

    # Handle game-specific actions if we aren't in a game over state.
    if not state.game_over:
        if action.rotate.cw:            # rotate clockwise
            next_pos.rotation += 1
            next_pos.rotation %= 4
            action.rotate.cw = False
        if action.rotate.ccw:           # rotate counter-clockwise
            next_pos.rotation -= 1
            next_pos.rotation %= 4
            action.rotate.ccw = False
        if action.move.left:            # move left
            next_pos.column -= 1
        if action.move.right:           # move right
            next_pos.column += 1
        if action.move.down:            # move down
            next_pos.row += 1

        # Make the proposed move if we can.
        if is_valid_move(next_pos, tetro):
            EmptyObject.field_copy(pos, next_pos)

    # Handle gravity if it is time to do so.
    if gravity_event.poll():
        pos.row += 1        # move block down
        if not (is_valid_move(pos, tetro) or state.game_over):
            pos.row -= 1    # cancel out move if it can't be done

            # Count this block.
            state.player.block_count += 1
            state.player.score += config.scoring.DROP_BLOCK
            print(f"Score: {state.player.score}")

            # Place the piece on the board.  If a game over state
            # was triggered from selecting this block, we will still
            # place it on the board to give a visual cue that we can't
            # place it anywhere.
            playing_field.place_piece_nocheck(pos, tetro)

            # Check for lines.  Because only one block is being
            # placed at a time, the only place where lines could
            # be created is in the area where the last block was
            # placed.
            for drow in tetro.height_range:
                r_board = playing_field[pos.row + drow]

                # Is this a valid row that's completely full?
                # If so, then track the row, and mark all cells
                # in the row with a color effect that updates
                # every frame.
                if r_board and all(r_board):
                    state.current_rows_cleared.append(pos.row + drow)
                    r_board[:] = [state.color.line_clear] * len(r_board)

            # Did we clear any rows?  Keep track of them and update the score.
            if state.current_rows_cleared:
                nlines = len(state.current_rows_cleared)
                points = config.scoring.CLEAR_LINE(nlines)

                state.player.line_count += nlines
                state.player.score += points

                print(f"Cleared {nlines} line(s) for {points} points\n")
                print(f"Score: {state.player.score}")

                # Only draw for the next few frames for the effect.
                state.next_frame_draw_only = config.LINE_CLEAR_FRAME_DELAY

                # Is it time to go to the next level?
                if state.player.line_count >= state.next_level_lines:
                    state.next_level_lines += config.LINES_PER_LEVEL
                    gravity_event.limit -= 1

                    level = config.GRAVITY_FRAME_DELAY_START
                    level -= gravity_event.limit
                    level += 1

                    print(f"----- Level {level} -----")

            # We're done with our piece, we can now let go of it.
            # This will allow us to retrieve the next block at the
            # start of the next frame.
            block.current_index = 0

    # Handle the game over effect.
    if state.game_over:
        _game_over_effect(state)
