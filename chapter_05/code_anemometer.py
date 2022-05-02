import time
import board
import countio

with countio.Counter(board.GP15) as pin_counter:
    last_tick = time.monotonic()
    while True:
        if pin_counter.count and ((time.monotonic() - last_tick) > 1.0):
            print("Wind Speed = {0} mph".format(pin_counter.count * 1.492))
            pin_counter.reset()
            last_tick = time.monotonic()
