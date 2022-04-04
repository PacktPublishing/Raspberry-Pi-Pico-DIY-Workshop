import sys
from time import sleep
import board
import busio
import sparkfun_qwiickeypad

i2c = busio.I2C(board.GP9, board.GP8)
# Create keypad object
keypad = sparkfun_qwiickeypad.Sparkfun_QwiicKeypad(i2c)

print("Qwiic Keypad Simple Test")

# Check if connected
if keypad.connected:
    print("Keypad connected. Firmware: ", keypad.version)
else:
    print("Keypad does not appear to be connected. Please check wiring.")
    sys.exit()

print("Press any button on the keypad.")

# button value -1 is error/busy, 0 is no key pressed
button = -1

# while no key is pressed
while True:
    # request a button
    keypad.update_fifo()
    button = keypad.button
    # Display the button value
    if button > 0:
        print("Button '" + chr(button) + "' was pressed.")
    # wait a bit before trying again
    sleep(0.100
