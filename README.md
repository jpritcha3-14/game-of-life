# Conway's Game of Life

This is a graphical implementation of [Conway's cellular automaton](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).  The game is played by creating an initial seed and seeing how it evolves over time.  At each time step (generation) the cells states (alive or dead) are updated according to the following rules

1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

## Dependencies
The only package required to run the game (other than Python 3) is [pygame](https://www.pygame.org/wiki/about).

It can be installed via pip:
`pip install pygame`


## Instructions
+ Click the board to change the state of an individual cell.
+ Click and drag on the board to change states of multiple cells.
	+ To seed cells, start click and drag on a dead cell.
	+ To kill cells, start click and drag on a live cell.
+ Click the start button to begin the game, press it again to stop.
+ Click the clear button to clear the board and stop the game.
