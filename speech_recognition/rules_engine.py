# %% Libraries

import chess
import chess.svg
from IPython.display import SVG
import speech
import time

def make_move(board, move):
    if board.is_checkmate():
        print("Checkmate")

    # if board.turn():
    #     print("White's move: \n")
    # else:
    #     print("Black's move: \n")
    
    # moves = board.legal_moves
    s = str(board.legal_moves)
    s = s[s.find("(")+1:s.find(")")]
    try:
        #move = input("Enter a move: ")
        
        square_diction = board.parse_san(move)
        is_cap = board.is_capture(square_diction)

        board.push_san(move)

        gantry_move_format = (square_diction.uci()[:2], square_diction.uci()[2:], is_cap)
        print(gantry_move_format)
        print(board)
    except ValueError:
        print("\nEnter a valid move...")
    



