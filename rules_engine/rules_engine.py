# %% Libraries

import chess
import chess.svg
from IPython.display import SVG
import speech
import time

board = chess.Board()
# print(board.legal_moves)
# print([move for move in board.legal_moves])

# %%
is_white = True
while not board.is_checkmate():
    #print("")
    if is_white:
        print("White's move: \n")
    else:
        print("Black's move: \n")
    
    # moves = board.legal_moves
    s = str(board.legal_moves)
    s = s[s.find("(")+1:s.find(")")]
    try:
        print(board)
        print("")
        print(s)
        print("")
        print("Pausing for 10 seconds... Pick a move!")
        # time.sleep(10)
        move = speech.getMoveFromAudio()

        #move = input("Enter a move: ")
        square_diction = board.parse_san(move)
        is_cap = board.is_capture(square_diction)

        board.push_san(move)

        gantry_move_format = (square_diction.uci()[:2], square_diction.uci()[2:], is_cap)
        print(gantry_move_format)
    except ValueError:
        print("\nEnter a valid move...")
        continue
        

    is_white = not is_white

color = "White"
if is_white:
    color = "Black"

print(board)
print(f"\nCheckmate, {color} wins!")


