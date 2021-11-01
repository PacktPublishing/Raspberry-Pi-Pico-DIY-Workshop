import board
import busio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

while True:
    # capture message
    message = input("Enter a message:").encode("utf-8")
    uart.write(message)
    # receive echo
    bytes_waiting = uart.in_waiting
    if bytes_waiting:
        incoming_msg = uart.read(bytes_waiting)
        print(incoming_msg)