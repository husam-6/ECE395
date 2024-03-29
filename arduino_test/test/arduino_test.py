# %% Libraries
import pyfirmata
import time

MOTOR_1 = 1
MOTOR_2 = 2
MOTOR_1_PINS = (2, 4)       # (DIR, STEP)
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
        #print(f"LIMIT SWITCH INPUT: {board.analog[ANALOG_PIN].read()}")
        if (board.analog[ANALOG_PIN1].read() != 0 and _dir == 1 and motor == MOTOR_1) or (board.analog[ANALOG_PIN2].read() != 0 and _dir == 0 and motor == MOTOR_1) or (board.analog[ANALOG_PIN3].read() != 0 and _dir == 0 and motor == MOTOR_2) or (board.analog[ANALOG_PIN4].read() != 0 and _dir == 1 and motor == MOTOR_2):
            print("LIMIT SWITCH HIT" )
            # print(f"LIMIT SWITCH: {board.analog[ANALOG_PIN1].read()}")
            # print(f"LIMIT SWITCH: {board.analog[ANALOG_PIN2].read()}")
            return
        

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


def test_both():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    move_diagonal(direc, direc, num_squares=squares)
    board.pass_time(1)


def test_one_at_time():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    motor = int(input("Enter motor to move: "))
    print(f"Running motor {motor}")
    move_num_squares(motor, direc, squares)

# For limit switches
ANALOG_PIN1 = 5
ANALOG_PIN2 = 0
ANALOG_PIN3 = 2
ANALOG_PIN4 = 3

it = pyfirmata.util.Iterator(board)
board.analog[ANALOG_PIN1].enable_reporting()
it.start()

# it2 = pyfirmata.util.Iterator(board)
board.analog[ANALOG_PIN2].enable_reporting()
board.analog[ANALOG_PIN3].enable_reporting()
board.analog[ANALOG_PIN4].enable_reporting()
# it2.start()

while True:
    choice = int(input("Test one motor (1) at a time or both (2)? Enter 1 or 2: "))
    if (choice == 2):
        test_both()
    else:
        test_one_at_time()
    # print(f"LIMIT 1: {board.analog[ANALOG_PIN1].read()}, Limit 2: {board.analog[ANALOG_PIN2].read()}, Limit 3: {board.analog[ANALOG_PIN3].read()}, Limit 4: {board.analog[ANALOG_PIN4].read()}")
    board.pass_time(0.05)
