# Write your code here :-)
import board
import busio
import time
from digitalio import DigitalInOut, Direction, Pull

latch = DigitalInOut(board.GP17)
clock = DigitalInOut(board.GP18)
data = DigitalInOut(board.GP19)

latch.direction = Direction.OUTPUT
clock.direction = Direction.OUTPUT
data.direction = Direction.OUTPUT

latch.value = False
clock.value = False
data.value = False


def post_number(number, decimal=False):
    a = 1<<0
    b = 1<<6
    c = 1<<5
    d = 1<<4
    e = 1<<3
    f = 1<<1
    g = 1<<2
    dp = 1<<7

    if number == 1: segments = b | c
    elif number == 2: segments = a | b | d | e | g
    elif number == 3: segments = a | b | c | d | g
    elif number == 4: segments = f | g | b | c
    elif number == 5: segments = a | f | g | c | d
    elif number == 6: segments = a | f | g | e | c | d
    elif number == 7: segments = a | b | c
    elif number == 8: segments = a | b | c | d | e | f | g
    elif number == 9: segments = a | b | c | d | f | g
    elif number == 0: segments = a | b | c | d | e | f
    elif number == " ": segments = 0
    elif number == "c": segments = g | e | d
    elif number == "-": segments = g
    else: segments = 0

    if decimal: segments |= dp

    for i in range(8):
        clock.value = False
        data.value = segments & (1 << (7 - i))
        clock.value = True

x = 0

while True:
    if x == 9:
        post_number(x, True)
    else:
        post_number(x, False)

    latch.value = False
    latch.value = True
    time.sleep(0.5)

    x += 1
    x %= 10

    print(x)





