## Principles of Computing (Part 1)
## Mini-project 3: Tic-Tac-Toe (Monte Carlo)
## MonteCarlo_TicTacToe.py

## Module was initially intended to be run with CodeSkulptor http://www.codeskulptor.org/#poc_ttt_template.py


"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    empty_cells_list = board.get_empty_squares()
    while not board.check_win():
        random_choice = random.randrange(len(empty_cells_list))
        board.move(empty_cells_list[random_choice][0], 
                          empty_cells_list[random_choice][1],
                          player)
        player = provided.switch_player(player)


def mc_update_scores(scores, board, player):
    opponent = provided.switch_player(player)
    if player == board.check_win():
        me_winner = True
    elif opponent == board.check_win():
        me_winner = False
    else:
        return 0
    for index_row, row in enumerate(scores):
        for index_col, _col in enumerate(row):
            current_cell = board.square(index_row, index_col)
            if current_cell == player:
                if me_winner:
                    scores[index_row][index_col] += SCORE_CURRENT
                else: 
                    scores[index_row][index_col] -= SCORE_CURRENT
            elif current_cell == provided.switch_player(player):
                if me_winner:
                    scores[index_row][index_col] -= SCORE_OTHER
                else: 
                    scores[index_row][index_col] += SCORE_OTHER


def get_best_move(board, scores):
    empty_cells = board.get_empty_squares()
    scores_dict = {}
    for _idx, cell in enumerate(empty_cells):
        scores_dict[cell] = scores[cell[0]][cell[1]]
    max_score = max(scores_dict.values())
    max_scores_list = [x for x,y in scores_dict.items() 
                       if y == max_score]
    choice = random.randrange(len(max_scores_list))
    return max_scores_list[choice]


def mc_move(board, player, trials):
    scores = [[0 for dummycol in range(board.get_dim())] 
                 for dummyrow in range(board.get_dim())]
    for _trial in range(trials):
        board_to_try = board.clone()
        mc_trial(board_to_try, player)
        mc_update_scores(scores, board_to_try, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)