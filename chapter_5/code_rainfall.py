import time
import board
import countio

with countio.Counter(board.GP15) as pin_counter:
    while True:
        if pin_counter.count:
            print("Rainfall Detected")
            pin_counter.reset()
            time.sleep(2)

