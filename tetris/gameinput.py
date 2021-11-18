import pygame


# process_input_and_events ################################
def process_input_and_events(state):

    # Aliases.
    draw_only = state.next_frame_draw_only > 0
    action = state.action

    # Check events
    for event in pygame.event.get():

        # Is the user closing the window?
        if event.type == pygame.QUIT:
            state.running = False

        # Is the user holding down a key?
        elif event.type == pygame.KEYDOWN:

            # Enable the following inputs if this
            # frame isn't a "drawing only" frame.
            if not draw_only:

                # P for pause
                if event.key == pygame.K_p:
                    state.paused = not state.paused

                # Up arrow for 90 degree clockwise rotation.
                # We handle this event here because we don't want
                # the player holding down the up arrow key to trigger
                # multiple rotation events.
                if event.key == pygame.K_UP:

                    # These get set back to False in
                    # the block of code that handles them.
                    if event.mod & pygame.KMOD_SHIFT:   # Hold shift for
                        action.rotate.ccw = True        # counterclockwise.
                    else:
                        action.rotate.cw = True

    # If we're only drawing, disable all moving-related actions.
    if draw_only:
        action.move.left = False
        action.move.right = False
        action.move.down = False

    # Otherwise, translate keypresses into values that can
    # be processed by the game logic.  If you look at the
    # game logic module, you will notice that *no* pygame
    # routines are used.  This separation is deliberate and
    # allows a different multimedia or graphics engine to be
    # used if I feel like changing it later.
    else:
        keys = pygame.key.get_pressed()

        action.move.left = keys[pygame.K_LEFT]
        action.move.right = keys[pygame.K_RIGHT]
        action.move.down = keys[pygame.K_DOWN]

    # Return whether or not we're still running.
    return state.running
