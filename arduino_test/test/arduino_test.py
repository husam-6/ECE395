# %% Libraries
import pyfirmata
import time

MOTOR_1 = 1
MOTOR_2 = 2
MOTOR_1_PINS = (3, 4)       # (DIR, STEP)
MOTOR_2_PINS = (5, 6)       # (DIR, STEP)

DELAY = 400e-6
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')
print("Communication Successfully started")


def move_num_squares(motor=MOTOR_1, _dir=1, num_squares=1):
    """ Rotate stepper motor 1 full revolution"""

    # For now, assume moving 1 square is 1 full revolution
    bound = num_squares * 800

    dir_pin, step_pin = MOTOR_1_PINS
    if motor == MOTOR_2:
        dir_pin, step_pin = MOTOR_2_PINS
    
    board.digital[dir_pin].write(_dir)
    # 800 pulses = 1 revolution
    for i in range(bound):
        board.digital[step_pin].write(1)
        board.pass_time(DELAY)
        # time.sleep(DELAY)
        board.digital[step_pin].write(0)
        # time.sleep(DELAY)
        board.pass_time(DELAY)


def move_diagonal(_dir_1=1, _dir_2=1, num_squares=1):
    """ Rotate both motors"""

    # For now, assume moving 1 square is 1 full revolution
    bound = num_squares * 800

    dir_pin_1, step_pin_1 = MOTOR_1_PINS
    dir_pin_2, step_pin_2 = MOTOR_2_PINS
    
    board.digital[dir_pin_1].write(_dir_1)
    board.digital[dir_pin_2].write(_dir_2)
    # 800 pulses = 1 revolution
    for i in range(bound):
        board.digital[step_pin_1].write(1)
        board.digital[step_pin_2].write(1)
        board.pass_time(DELAY)
        # time.sleep(DELAY)
        board.digital[step_pin_1].write(0)
        board.digital[step_pin_2].write(0)
        # time.sleep(DELAY)
        board.pass_time(DELAY)




while True:
    print("Running motor 1")
    squares = int(input("Enter number of squares to move: "))
    move_diagonal(1, 1, squares)
    board.pass_time(1)
    # move_num_squares(MOTOR_1, 1, squares)
    # board.pass_time(1)
    # # move_num_squares(MOTOR_1, 0, squares)
    # print("Running motor 2")
    # move_num_squares(MOTOR_2, 1, squares)
    # board.pass_time(1)


