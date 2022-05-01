import time
import board
import busio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

while True:
    # await incoming message
    bytes_waiting = uart.in_waiting
    if bytes_waiting:
        incoming_msg = uart.readline()
        print(incoming_msg)
        # re-transmit
        uart.write(incoming_msg)