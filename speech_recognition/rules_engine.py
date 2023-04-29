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
import logging
import time
import os 

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


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

START_X = 1.15 + 3       # fix offset from edge of the board, move 3 squares to a1 square
START_Y = 0.875

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
        
    
#     print("Move " + str(num_squares) + " " + tmp)

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
        #check if en passant
        if m[4] and int(m[1][1]) == 6:
            end_coord = (mapping[m[1][0]], int(m[1][1]) - 2)    
        elif m[4] and int(m[1][1]) == 3:
            end_coord = (mapping[m[1][0]], int(m[1][1]))

        # Go to end_coord, raise magnet
        # Go down 1/2, then off the board
        # Then go back to start_coord
        move_num_squares(1, 1, end_coord[0])
        move_num_squares(2, 1, end_coord[1])
        magnet_on()

        # Move piece off the board
        # print(board.turn)
        if board.turn:
            move_num_squares(2, 0, 1/2)
            time.sleep(.5)
            move_num_squares(1, 0, end_coord[0] + 3)
            magnet_off()

            # Move to start square
            move_num_squares_helper(start_coord[0] + 3, True)
            time.sleep(.5)
            move_num_squares_helper(start_coord[1] - (end_coord[1] - 1/2), False)
            magnet_on()
        else:
            move_num_squares(2, 0, 1/2)
            time.sleep(.5)
            move_num_squares(1, 1, 7 - end_coord[0] + 3)
            magnet_off()

            # Move to start square
            move_num_squares_helper(start_coord[0] - 10, True)
            time.sleep(.5)
            move_num_squares_helper(start_coord[1] - (end_coord[1] - 1/2), False)
            magnet_on()
    
        # To fix en passant end square
        end_coord = (mapping[m[1][0]], int(m[1][1]) - 1)

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
            time.sleep(0.5)
            move_num_squares_helper(end_coord[1] - start_coord[1], False)
            time.sleep(0.5)
            move_num_squares_helper((end_coord[0] - start_coord[0]) / 2, True)
        else:
            move_num_squares_helper((end_coord[1] - start_coord[1]) / 2, False)
            time.sleep(0.5)
            move_num_squares_helper(end_coord[0] - start_coord[0], True)
            time.sleep(0.5)
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
        time.sleep(0.5)
        move_num_squares(1, 0, 2)
        time.sleep(0.5)
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
        time.sleep(0.5)
        move_num_squares(1, 1, 3)
        time.sleep(0.5)
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
        
        # Check if pawn promotion to Queen
        if m[5]:
            # Move pawn off board and get queen
            if not board.turn:
                time.sleep(1)
                move_num_squares(2, 0, 1/2)
                move_num_squares(1, 0, end_coord[0] + 3)
                magnet_off()
                move_num_squares(2, 1, 1/2)
                move_num_squares(1, 1, 1)
                magnet_on()
                move_num_squares(2, 0, 1/2)
                move_num_squares(1, 1, end_coord[0] + 2)
                move_num_squares(2, 1, 1/2)

            else:
                time.sleep(1)
                move_num_squares(2, 0, 1/2)
                move_num_squares(1, 1, 7 - end_coord[0] + 3)
                magnet_off()
                move_num_squares(2, 1, 1/2)
                move_num_squares(1, 0, 1)
                magnet_on()
                move_num_squares(2, 0, 1/2)
                move_num_squares(1, 0, 7 - end_coord[0] + 2)
                move_num_squares(2, 1, 1/2)
                



        # Turn magnet off and go to baseline square
        magnet_off()
        move_num_squares(1, 0, end_coord[0])
        move_num_squares(2, 0, end_coord[1])
        

def make_move(board, move):

    if board.turn:
        logging.info("White's move: \n")
        arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('WHITE TO MOVE!'))
    else:
        logging.info("Black's move: \n")
        arduino_control.board.send_sysex(arduino_control.STRING_DATA, arduino_control.util.str_to_two_byte_iter('BLACK TO MOVE!'))
    
    # moves = board.legal_moves

    try:
        #move = input("Enter a move: ")
        
        square_diction = board.parse_san(move)

        promotion = False
        if len(square_diction.uci()) == 5 and square_diction.uci()[4] == 'q':
            promotion = True

        is_cap = board.is_capture(square_diction)
        logging.info(f"Attempted move: {move}")

        en_passant = board.is_en_passant(chess.Move.from_uci(square_diction.uci()))

        board.push_san(move)

        gantry_move_format = (square_diction.uci()[:2], square_diction.uci()[2:4], is_cap, board.piece_at(chess.parse_square(square_diction.uci()[2:4])).piece_type, en_passant, promotion)
        
        s = str(board.legal_moves)
        s = s[s.find("(")+1:s.find(")")]

        logging.info(gantry_move_format)
        logging.info(f"\n{board}")
        logging.info(s)

        execute_move(gantry_move_format)

    except ValueError:
        logging.info("\nEnter a valid move...")
    
    if board.is_checkmate():
        logging.info("Checkmate!")
        exit(2)

    # os._exit(1)

# Initialization 
# Get to start square by going to edge of board
move_num_squares(1, 0, 300)
move_num_squares(2, 0, 300)

# Move to start squares
move_num_squares(1, 1, START_X)
move_num_squares(2, 1, START_Y)

# Temporary for path algo testing
# board = chess.Board(fen="rnbqkbnr/pPpppp1p/8/8/8/8/P1PPPPpP/RNBQKBNR w KQkq - 0 1")
board = chess.Board()
logging.info(f"\n{board}")

if __name__ == "__main__":
    while(True):
        move = input("What is your chess move?\n")
        make_move(board, move)


