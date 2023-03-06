# %% Libraries
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/cu.usbmodem14401')

while True:
    print("Running")
    # for i in range(0,1600):
    board.digital[3].write(1)
    time.sleep(1)
    board.digital[3].write(0)
    time.sleep(1)
