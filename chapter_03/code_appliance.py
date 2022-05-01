import board
import digitalio
import time

switch = digitalio.DigitalInOut(board.D12)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

relay = digitalio.DigitalInOut(board.D11)
relay.direction = digitalio.Direction.OUTPUT

while True:
    if switch.value:
        relay.value = True
    else:
        relay.value = False
    time.sleep(1)


