# %% Libraries
import pyfirmata
import time

MOTOR_1 = 1
MOTOR_2 = 2
MOTOR_1_PINS = (2, 4)       # (DIR, STEP)
MOTOR_2_PINS = (5, 6)       # (DIR, STEP)
MAGNET_PIN = 9

DELAY = 400e-6
board = pyfirmata.Arduino('/dev/cu.usbmodem14101')
print("Communication Successfully started")
print("Initializing limit switch params")

# For limit switches
LIMIT_1 = 12
LIMIT_2 = 11
LIMIT_3 = 10
LIMIT_4 = 13


board.digital[LIMIT_1].mode = pyfirmata.INPUT
board.digital[LIMIT_2].mode = pyfirmata.INPUT
board.digital[LIMIT_3].mode = pyfirmata.INPUT
board.digital[LIMIT_4].mode = pyfirmata.INPUT
it = pyfirmata.util.Iterator(board)
it.start()

# ANALOG_PIN1 = 5
# ANALOG_PIN2 = 0             
# ANALOG_PIN3 = 1             
# ANALOG_PIN4 = 3             

# it2 = pyfirmata.util.Iterator(board)
# board.analog[ANALOG_PIN1].enable_reporting()
# board.analog[ANALOG_PIN2].enable_reporting()
# board.analog[ANALOG_PIN3].enable_reporting()
# board.analog[ANALOG_PIN4].enable_reporting() 
board.pass_time(1)
# it2.start()


def move_num_squares(motor=MOTOR_1, _dir=1, num_squares=1):
    """ Rotate stepper motor 1 full revolution"""

    # For now, assume moving 1 square is 1 full revolution
    bound = int(num_squares * 800 / 1.5)

    dir_pin, step_pin = MOTOR_1_PINS
    if motor == MOTOR_2:
        dir_pin, step_pin = MOTOR_2_PINS
    
    board.digital[dir_pin].write(_dir)
    # 800 pulses = 1 revolution
    for i in range(bound):
        #print(f"LIMIT SWITCH INPUT: {board.analog[ANALOG_PIN].read()}")
        if (board.digital[LIMIT_1].read() and _dir == 1 and motor == MOTOR_1) or (board.digital[LIMIT_2].read() and _dir == 0 and motor == MOTOR_1) or (board.digital[LIMIT_3].read() and _dir == 0 and motor == MOTOR_2) or (board.digital[LIMIT_4].read() and _dir == 1 and motor == MOTOR_2):
            print("LIMIT SWITCH HIT" )
            print(f"LIMIT 1: {board.digital[LIMIT_1].read()}, Limit 2: {board.digital[LIMIT_2].read()}, Limit 3: {board.digital[LIMIT_3].read()}, Limit 4: {board.digital[LIMIT_4].read()}")
            board.pass_time(1)
            # print(f"LIMIT SWITCH: {board.digital[ANALOG_PIN1].read()}")
            # print(f"LIMIT SWITCH: {board.digital[ANALOG_PIN2].read()}")
            return
        

        board.digital[step_pin].write(1)
        board.pass_time(DELAY)
        # time.sleep(DELAY)
        board.digital[step_pin].write(0)
        # time.sleep(DELAY)
        board.pass_time(DELAY)


def move_num_squares_diagonal(_dir_1=1, _dir_2=1, num_squares=1):
    """ Rotate both motors"""

    # For now, assume moving 1 square is 1 full revolution
    bound = int(num_squares * 800 / 1.5)

    dir_pin_1, step_pin_1 = MOTOR_1_PINS
    dir_pin_2, step_pin_2 = MOTOR_2_PINS
    
    board.digital[dir_pin_1].write(_dir_1)
    board.digital[dir_pin_2].write(_dir_2)
    # 800 pulses = 1 revolution
    for i in range(bound):
        if board.digital[LIMIT_1].read() or board.digital[LIMIT_2].read() or board.digital[LIMIT_3].read() or board.digital[LIMIT_4].read():
            print("LIMIT SWITCH HIT" )
            board.pass_time(1)
            return
        board.digital[step_pin_1].write(1)
        board.digital[step_pin_2].write(1)
        board.pass_time(DELAY)
        # time.sleep(DELAY)
        board.digital[step_pin_1].write(0)
        board.digital[step_pin_2].write(0)
        # time.sleep(DELAY)
        board.pass_time(DELAY)

def magnet_on():
    board.digital[MAGNET_PIN].write(1)
    board.pass_time(1)

def magnet_off():
    board.digital[MAGNET_PIN].write(0)
    board.pass_time(1)

def test_both():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    move_num_squares_diagonal(direc, direc, num_squares=squares)
    board.pass_time(1)


def test_one_at_time():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    motor = int(input("Enter motor to move: "))
    print(f"Running motor {motor}")
    move_num_squares(motor, direc, squares)

if __name__ == "__main__":
    # magnet_on()
    while True:
        choice = int(input("Test one motor (1) at a time or both (2) or magnet 3? Enter 1 or 2 or 3 or 4: "))
        if (choice == 2):
            test_both()
        elif choice == 3:
            magnet_on()
            board.pass_time(5)
        elif choice == 4:
            magnet_off()
        else:
            test_one_at_time()
        # print(f"LIMIT 1: {board.digital[LIMIT_1].read()}, LIMIT 2: {board.digital[LIMIT_2].read()}, LIMIT 3: {board.digital[LIMIT_3].read()}, Limit 4: {board.digital[LIMIT_4].read()}")
        board.pass_time(0.05)
