import board
import digitalio
import time

switch = digitalio.DigitalInOut(board.D12)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

while True:
    print(switch.value)
    time.sleep(1)

