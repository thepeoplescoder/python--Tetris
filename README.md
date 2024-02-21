# Tetris

A basic implementation of Tetris in Python.

## Why Write It?

I originally wrote this in 2019, to learn the basics of
[pygame][pygame-github].  The project was a little
[rushed](#project-roadmap), as I wanted to get a feel for
how pygame works, and make something playable as soon as
possible.

## Requirements

1. This game has been tested on [Python 3.9][python-3-9-download],
   so having that version installed would be ideal.  I have yet to
   test on other versions of Python.
   * _If you're worried about this conflicting with your currently
     installed version of Python and you've never heard of either
     [pyenv][pyenv-github] or [pyenv-win][pyenv-win-github] (Windows
     version of pyenv), I recommend checking them out!  They allow
     you to run multiple installations of Python side by side._

2. Since [pygame][pygame-homepage] is used, make sure that
   you have the required pygame dependencies installed for
   your platform.

3. Dependencies are managed via [Pipenv][pipenv-homepage], so be
   sure to have it
   [installed](https://pipenv.pypa.io/en/latest/installation.html)
   as well.
   * _I personally use [pipx](https://github.com/pypa/pipx)
    to install Pipenv._

## How to Run

Please see the [controls](#controls) on how to play.\
These steps assume the requirements [above](#requirements)
are met:

1. Clone this repository and change into the directory,
   if you haven't done so already:

   ```sh
   # Cloning to ./Tetris isn't mandatory, just makes things a little easier
   git clone https://github.com/thepeoplescoder/python--Tetris Tetris
   cd Tetris
   ```

2. Set up the environment:

   ```sh
   pipenv install
   ```

3. Run `main.py` inside of the repository _(now pipenv environment)_:

   ```sh
   pipenv run python main.py
   ```

## Controls

* Left and right arrows move the current block side to side
* Down arrow accelerates the current block downward
* Up arrow rotates the current block clockwise
* Shift+Up arrow rotates the current block counterclockwise
* P pauses/unpauses the game

## Current Features

* Lines clear with a randomized greyscale effect
* An area showing the next block to drop is displayed
  * _(it also rotates!)_
* Grid fills with random colors on game over
* Next block area fills with random shades of purple
  on game over

## Project Roadmap
* Codebase modifications
  * Ultimately make the code more self-documenting
  * Add an abstraction layer between pygame and the game logic to
    allow for the use of other graphics/game libraries, such as
    [arcade][arcade-github]
* "Beautify" the game a little bit more:
  * Label the area that displays the next block.
  * Display the score inside of the game window,
    instead of keeping track of it on the console.
  * Display the number of cleared lines in the game window.
  * Display the number of dropped blocks in the game window.
  * Update the display when the game is paused, such that
    the player knows without a doubt that the game is paused.
* Bugs
  * Levels advance (and therefore, speed increases) based on
    score, instead of on number of lines cleared.

[pygame-github]:       https://github.com/pygame/pygame
[pygame-homepage]:     https://pygame.org/
[pipenv-homepage]:     https://pipenv.pypa.io/en/latest/
[python-3-9-download]: https://www.python.org/downloads/release/python-3918/
[pyenv-github]:        https://github.com/pyenv/pyenv
[pyenv-win-github]:    https://github.com/pyenv-win/pyenv-win
[arcade-github]:       https://github.com/pythonarcade/arcade