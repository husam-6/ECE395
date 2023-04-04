# %% Libraries


# importing sys
import sys

# adding Folder_2/subfolder to the system path

from numpy import square
import chess
import chess.svg
import arduino_control 
from arduino_control import move_num_squares, move_num_squares_diagonal, magnet_on, magnet_off
# from IPython.display import SVG
# import speech
import time
import os

mapping = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}
baseline_coord = (0,0)

START_X = 1
START_Y = 1

# TEMPORARY FUNCTIONS FOR PRINTING
# Motor 1 = moves x axis
# Motor 2 = moves y axis
# Direction: 1 means to the right (or up), 0 means to the left (or down)
# def move_num_squares(motor=1, _dir=1, num_squares=1):
#     tmp = "Up"
#     if motor == 1:
#         if _dir == 1:
#             tmp = "Right"
#         else:
#             tmp = "Left"
#     else:
#         if _dir == 0:
#             tmp = "Down"
        
    
    # print("Move " + str(num_squares) + " " + tmp)

# def move_num_squares_diagonal(_dir_1=1, _dir_2=1, num_squares=1):
#     tmp = "Up-Left"
#     if _dir_1 == 1:
#         if _dir_2 == 1:
#             tmp = "Up-Right"
#         else:
#             tmp = "Down-Right"
#     else:
#         if _dir_2 == 0:
#             tmp = "Down-Left"
            
#     print("Move " + str(num_squares) + " " + tmp)
    
# def magnet_on():
#     print("Magnet On")

# def magnet_off():
#     print("Magnet Off")
  
  
# PERMANENT FUNCTIONS
def move_num_squares_helper(distance, x_dir):
    if x_dir:
        if distance < 0:
            move_num_squares(1, 0, abs(distance))
        else:
            move_num_squares(1, 1, distance)
    else:
        if distance < 0:
            move_num_squares(2, 0, abs(distance))
        else:
            move_num_squares(2, 1, distance)

def move_num_squares_diagnol_helper(x_val, y_val):
    if x_val < 0:
        if y_val < 0:
            move_num_squares_diagonal(0, 0, abs(x_val))
        else:
            move_num_squares_diagonal(0, 1, abs(x_val))
    else:
        if y_val < 0:
            move_num_squares_diagonal(1, 0, abs(x_val))
        else:
            move_num_squares_diagonal(1, 1, abs(x_val))

# Assume we start in the middle of square a1 (bottom left of the board)
def execute_move(m):
    start_coord = (mapping[m[0][0]], int(m[0][1]) - 1)
    end_coord = (mapping[m[1][0]], int(m[1][1]) - 1)
    
    if m[2]:
        # Go to end_coord, raise magnet
        # Go down 1/2, then off the board
        # Then go back to start_coord
        move_num_squares(1, 1, end_coord[0])
        move_num_squares(2, 1, end_coord[1])
        magnet_on()

        # Move piece off the board
        move_num_squares(2, 0, 1/2)
        move_num_squares(1, 0, end_coord[0] + 1)
        magnet_off()

        # Move to start square
        move_num_squares_helper(start_coord[0] + 1, True)
        move_num_squares_helper(start_coord[1] - (end_coord[1] - 1/2), False)
        magnet_on()

    # Go to start square and raise magnet
    else:
        move_num_squares(1, 1, start_coord[0])
        move_num_squares(2, 1, start_coord[1])
        magnet_on()
    
    # Check if knight
    if m[3] == 2:
        # Move Knight
        if abs(end_coord[0] - start_coord[0]) == 1:
            move_num_squares_helper((end_coord[0] - start_coord[0]) / 2, True)
            move_num_squares_helper(end_coord[1] - start_coord[1], False)
            move_num_squares_helper((end_coord[0] - start_coord[0]) / 2, True)
        else:
            move_num_squares_helper((end_coord[1] - start_coord[1]) / 2, False)
            move_num_squares_helper(end_coord[0] - start_coord[0], True)
            move_num_squares_helper((end_coord[1] - start_coord[1]) / 2, False)
            
        # Turn magnet off and go to baseline square
        magnet_off()
        move_num_squares(1, 0, end_coord[0])
        move_num_squares(2, 0, end_coord[1])
        
    # Check if kingside castle
    elif (m[3] == 6 and start_coord == (4, 0) and end_coord == (6, 0)) or (m[3] == 6 and start_coord == (4, 7) and end_coord == (6, 7)):
        move_num_squares(1, 1, 2)
        magnet_off()
        move_num_squares(1, 1, 1)
        magnet_on()
        move_num_squares(2, 0, .5)
        move_num_squares(1, 0, 2)
        move_num_squares(2, 1, .5)
        
        magnet_off()
        move_num_squares(1, 0, end_coord[0] - 1)
        move_num_squares(2, 0, end_coord[1])
         
    # Check if queenside castle
    elif (m[3] == 6 and start_coord == (4, 0) and end_coord == (2, 0)) or (m[3] == 6 and start_coord == (4, 7) and end_coord == (2, 7)):
        move_num_squares(1, 0, 2)
        magnet_off()
        move_num_squares(1, 0, 2)
        magnet_on()
        move_num_squares(2, 0, .5)
        move_num_squares(1, 1, 3)
        move_num_squares(2, 1, .5)
        
        magnet_off()
        move_num_squares(1, 0, end_coord[0] + 1)
        move_num_squares(2, 0, end_coord[1])
        
    else:
        # Move piece
        # Only y-movement
        if end_coord[0] - start_coord[0] == 0:
            move_num_squares_helper(end_coord[1] - start_coord[1], False)
        # Only x-movement
        elif end_coord[1] - start_coord[1] == 0:    
            move_num_squares_helper(end_coord[0] - start_coord[0], True)
        # Diagnol movement
        else:
            move_num_squares_diagnol_helper(end_coord[0] - start_coord[0], end_coord[1] - start_coord[1])
        
        # Turn magnet off and go to baseline square
        magnet_off()
        move_num_squares(1, 0, end_coord[0])
        move_num_squares(2, 0, end_coord[1])
        

def make_move(board, move):

    # if board.turn():
    #     print("White's move: \n")
    # else:
    #     print("Black's move: \n")
    
    # moves = board.legal_moves

    try:
        #move = input("Enter a move: ")
        
        square_diction = board.parse_san(move)
        is_cap = board.is_capture(square_diction)

        board.push_san(move)

        gantry_move_format = (square_diction.uci()[:2], square_diction.uci()[2:4], is_cap, board.piece_at(chess.parse_square(square_diction.uci()[2:4])).piece_type)
        s = str(board.legal_moves)
        s = s[s.find("(")+1:s.find(")")]
        print(gantry_move_format)
        print(board)
        print(s)
        execute_move(gantry_move_format)
    except ValueError:
        print("\nEnter a valid move...")
    
    if board.is_checkmate():
        print("Checkmate!")

    # os._exit(1)

# Get to start square by going to edge of board
move_num_squares(1, 0, 300)
move_num_squares(2, 0, 300)

move_num_squares(1, 1, START_X)
move_num_squares(2, 1, START_Y)

# Temporary for path algo testing
board = chess.Board()
print(board)

if __name__ == "__main__":
    while(True):
        move = input("What is your chess move?")
        make_move(board, move)


