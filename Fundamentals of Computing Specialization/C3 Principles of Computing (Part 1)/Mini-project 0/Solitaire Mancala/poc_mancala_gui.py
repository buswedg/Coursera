## Principles of Computing (Part 1)
## Mini-project 0: Solitaire Mancala
## SolitaireMancala.py

## Required packages:
## pygame - http://www.pygame.org/download.shtml
## SimpleGUICS2Pygame - https://simpleguics2pygame.readthedocs.org/

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#poc_mancala_gui.py
## In order to run on local Phython instance, call to import module 'simplegui' has been modified.


"""
GUI component of Mancala Solitaire
"""

import random
## import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Game and canvas constants
# Focus on boards with six houses and one store

BOARD_SIZE = 7
HOUSE_NUM = 120
TEXT_OFFSET = [0.3 * HOUSE_NUM, 0.7 * HOUSE_NUM]
CANVAS_SIZE = [BOARD_SIZE * HOUSE_NUM, HOUSE_NUM]

# all winnable games for six houses
WINNABLE_BOARDS = [[0, 0, 0, 0, 2, 4, 6], 
                    [0, 0, 0, 2, 4, 0, 0], 
                    [0, 0, 1, 1, 3, 5, 0], 
                    [0, 0, 1, 3, 0, 0, 0], 
                    [0, 0, 1, 3, 2, 4, 6], 
                    [0, 0, 2, 0, 0, 0, 0], 
                    [0, 0, 2, 0, 2, 4, 6], 
                    [0, 0, 2, 2, 4, 0, 0], 
                    [0, 1, 0, 0, 0, 0, 0], 
                    [0, 1, 0, 0, 2, 4, 6], 
                    [0, 1, 0, 2, 4, 0, 0], 
                    [0, 1, 1, 1, 3, 5, 0], 
                    [0, 1, 1, 3, 0, 0, 0], 
                    [0, 1, 1, 3, 2, 4, 6], 
                    [0, 1, 2, 0, 0, 0, 0], 
                    [0, 1, 2, 0, 2, 4, 6], 
                    [0, 1, 2, 2, 4, 0, 0]]


class MancalaGUI:
    """
    Container for interactive content
    """    

    def __init__(self, game):
        """ 
        Initializer to create frame, sets handlers and initialize game
        """
        self._frame = simplegui.create_frame("Mancala Solitaire", 
                                            CANVAS_SIZE[0], CANVAS_SIZE[1])
        self._frame.set_canvas_background("White")
        self._frame.set_draw_handler(self.draw)
        self._frame.add_button("New board", self.new_board, 200)
        self._frame.add_button("Restart board", self.restart_board, 200)
        self._frame.add_button("Make move", self.make_move, 200)
        self._frame.set_mouseclick_handler(self.click_move)
        
        # fire up game and frame
        self._game = game
        self.new_board()
        
    def start(self):
        """
        Start the GUI
        """
        self._frame.start()
        
    def restart_board(self):
        """
        Restart the game with the current configuration
        """
        self._game.set_board(self.start_board)
                   
    def new_board(self):
        """
        Restart the game with a new winnable baord
        """
        self.start_board = random.choice(WINNABLE_BOARDS)
        self.restart_board()
    
    def make_move(self):
        """
        Compute and apply next move for solver
        """
        self._game.apply_move(self._game.choose_move())    
        
    def click_move(self, pos):
        """
        Update game based on mouse click
        """
        move = (BOARD_SIZE - 1) - pos[0] // HOUSE_NUM
        self._game.apply_move(move)    
        
    def draw(self, canvas):
        """
        Handler for draw events, draw board
        """
        configuration = [self._game.get_num_seeds(house_num) for house_num in range(BOARD_SIZE)]
        current_text_pos = [(BOARD_SIZE - 1) * HOUSE_NUM + TEXT_OFFSET[0], TEXT_OFFSET[1]]
        current_line_pos = [(BOARD_SIZE - 1) * HOUSE_NUM, 0]
        
        if self._game.is_game_won():
            store_color = "LightGreen"
        else:
            store_color = "Pink"
        
        canvas.draw_polygon([current_line_pos, 
                             [current_line_pos[0] + HOUSE_NUM, current_line_pos[1]],
                             [current_line_pos[0] + HOUSE_NUM, current_line_pos[1] + HOUSE_NUM],
                             [current_line_pos[0], current_line_pos[1] + HOUSE_NUM]], 
                            3, "Black", store_color)
        
        for num_seeds in configuration:
            canvas.draw_text(str(num_seeds), current_text_pos, 0.5 * HOUSE_NUM, "Black")
            canvas.draw_line(current_line_pos, [current_line_pos[0], 
                                                current_line_pos[1] + HOUSE_NUM], 2, "Black")
            current_text_pos[0] -= HOUSE_NUM
            current_line_pos[0] -= HOUSE_NUM

def run_gui(game):
    """
    Run GUI with given game
    """
    gui = MancalaGUI(game)
    gui.start()
