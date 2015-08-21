## Principles of Computing (Part 1)
## Mini-project 3: Tic-Tac-Toe (Monte Carlo)
## poc_ttt_provided.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#poc_ttt_provided.py


"""
Provided Code for Tic-Tac-Toe
"""

# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
 
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)] 
                           for row in range(dim)]
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
         """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = []

        # rows
        lines.extend(board)

        # cols
        cols = [[board[rowidx][colidx] for rowidx in dimrng]
                for colidx in dimrng]
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in dimrng]
        diag2 = [board[idx][dim - idx -1] 
                 for idx in dimrng]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None
            
    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)

def switch_player(player):
    """
    Convenience function to switch players.
    
    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None
    
    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        print (board)
        print ()
        
    # Print winner
    if winner == PLAYERX:
        print ("X wins!")
    elif winner == PLAYERO:
        print ("O wins!")
    elif winner == DRAW:
        print ("Tie!")
    else:
        print ("Error: unknown winner")