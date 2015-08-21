## Principles of Computing (Part 1)
## Mini-project 2: 2048 (Full)
## Full_2048.py

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#poc_2048_template.py


"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    newline = []
    item1 = 0
	
    while True:
        while item1 < len(line) and line[item1] == 0:
            item1 += 1
        if item1 >= len(line):
            break
        item2 = item1 + 1
        while item2 < len(line) and line[item2] == 0:
            item2 += 1
        if item2 >= len(line):
            newline.append(line[item1])
            break
        if line[item1] == line[item2]:
            newline.append(2 * line[item1])
            item1 = item2 + 1
        else:
            newline.append(line[item1])
            item1 = item2
			
    return newline + [0] * (len(line) - len(newline))

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = [[0] * self._width for row in range(self._height)]
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for row in range(self._height):
            for col in range(self._width):
                self._grid[row][col] = 0
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        out = ''
        for row in self._grid:
            for entry in row:
                out += str(entry) + '\t'
            out += '\n'
        return out

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == LEFT or direction == UP:
            row = 0
            col = 0
        if direction == RIGHT:
            row = 0
            col = self._width - 1
        if direction == DOWN:
            row = self._height - 1
            col = 0
        changed = 0
        while 0 <= row < self._height and 0 <= col < self._width:
            crow = row
            ccol = col
            line = []
            while 0 <= crow < self._height and 0 <= ccol < self._width:
                line += [self.get_tile(crow, ccol)]
                crow += OFFSETS[direction][0]
                ccol += OFFSETS[direction][1]
            crow = row
            ccol = col
            newline = merge(line)
            if newline != line:
                changed += 1
            item = 0
            while 0 <= crow < self._height and 0 <= ccol < self._width:
                self.set_tile(crow, ccol, newline[item])
                crow += OFFSETS[direction][0]
                ccol += OFFSETS[direction][1]
                item += 1
            row += 1 - abs(OFFSETS[direction][0])
            col += 1 - abs(OFFSETS[direction][1])
        if changed > 0:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.random() < 0.9:
            value = 2
        else:
            value = 4
        srow = scol = 0
        maxnum = 0.0
        for row in range(self._height):
            for col in range(self._width):
                if self.get_tile(row, col) == 0:
                    num = random.random()
                    if num > maxnum:
                        maxnum = num
                        srow = row
                        scol = col
        self.set_tile(srow, scol, value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
