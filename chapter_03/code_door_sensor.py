import board
import digitalio
import time

switch = digitalio.DigitalInOut(board.GP12)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

while True:
    print(switch.value)
    if not switch.value:
        print("Door Sensor activated")
    time.sleep(1)

