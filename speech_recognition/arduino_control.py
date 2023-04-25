# %% Libraries
import pyfirmata
import time
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

MOTOR_1 = 1
MOTOR_2 = 2
MOTOR_1_PINS = (2, 4)       # (DIR, STEP)
MOTOR_2_PINS = (5, 6)       # (DIR, STEP)
MAGNET_PIN = 9
STEPS_PER_SQ = 1.58

DELAY = 400e-6
logging.info("Attempting to connect to arduino...")
board = pyfirmata.Arduino('/dev/cu.usbmodem141101')
logging.info("Communication Successfully started")
logging.info("Initializing limit switch params")

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

board.pass_time(1)
# it2.start()


def move_num_squares(motor=MOTOR_1, _dir=1, num_squares=1):
    """ Rotate stepper motor 1 full revolution"""

    # For now, assume moving 1 square is 1 full revolution
    bound = int(num_squares * 800 / STEPS_PER_SQ)

    dir_pin, step_pin = MOTOR_1_PINS
    if motor == MOTOR_2:
        dir_pin, step_pin = MOTOR_2_PINS
    
    board.digital[dir_pin].write(_dir)
    # 800 pulses = 1 revolution
    for i in range(bound):
        #logging.info(f"LIMIT SWITCH INPUT: {board.analog[ANALOG_PIN].read()}")
        if (board.digital[LIMIT_1].read() and _dir == 1 and motor == MOTOR_1) or (board.digital[LIMIT_2].read() and _dir == 0 and motor == MOTOR_1) or (board.digital[LIMIT_3].read() and _dir == 0 and motor == MOTOR_2) or (board.digital[LIMIT_4].read() and _dir == 1 and motor == MOTOR_2):
            logging.info("LIMIT SWITCH HIT" )
            logging.info(f"LIMIT 1: {board.digital[LIMIT_1].read()}, Limit 2: {board.digital[LIMIT_2].read()}, Limit 3: {board.digital[LIMIT_3].read()}, Limit 4: {board.digital[LIMIT_4].read()}")
            board.pass_time(1)
            # logging.info(f"LIMIT SWITCH: {board.digital[ANALOG_PIN1].read()}")
            # logging.info(f"LIMIT SWITCH: {board.digital[ANALOG_PIN2].read()}")
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
    bound = int(num_squares * 800 / STEPS_PER_SQ)

    dir_pin_1, step_pin_1 = MOTOR_1_PINS
    dir_pin_2, step_pin_2 = MOTOR_2_PINS
    
    board.digital[dir_pin_1].write(_dir_1)
    board.digital[dir_pin_2].write(_dir_2)
    # 800 pulses = 1 revolution
    for i in range(bound):
        if board.digital[LIMIT_1].read() or board.digital[LIMIT_2].read() or board.digital[LIMIT_3].read() or board.digital[LIMIT_4].read():
            logging.info("LIMIT SWITCH HIT" )
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
    # Slow movement when we are moving a piece
    global DELAY
    DELAY = 800e-6
    board.digital[MAGNET_PIN].write(1)
    board.pass_time(2)

def magnet_off():
    # Reset delay to default
    global DELAY
    DELAY = 400e-6
    board.digital[MAGNET_PIN].write(0)
    board.pass_time(2)

def test_both():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    move_num_squares_diagonal(direc, direc, num_squares=squares)
    board.pass_time(1)


def test_one_at_time():
    squares = int(input("Enter number of squares to move: "))
    direc = int(input("Enter direction: "))
    motor = int(input("Enter motor to move: "))
    logging.info(f"Running motor {motor}")
    move_num_squares(motor, direc, squares)

if __name__ == "__main__":
    # magnet_on()
    while True:
        choice = int(input("Test one motor (1) \nBoth (2) \nMagnet on (3) \nMagnet off (4) \nTest limit switches (5)\n"))
        if (choice == 2):
            test_both()
        elif choice == 3:
            magnet_on()
            board.pass_time(5)
        elif choice == 4:
            magnet_off()
        elif choice == 5:
            while True:
                logging.info(f"LIMIT 1: {board.digital[LIMIT_1].read()}, LIMIT 2: {board.digital[LIMIT_2].read()}, LIMIT 3: {board.digital[LIMIT_3].read()}, Limit 4: {board.digital[LIMIT_4].read()}")
        else:
            test_one_at_time()
        board.pass_time(0.05)
