# A simple echo test for the Feather M0 Bluefruit
# Sets the name, then echo's all RX'd data with a reversed packet

import time
import busio
import board
from digitalio import DigitalInOut
from adafruit_bluefruitspi import BluefruitSPI

spi_bus = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = DigitalInOut(board.GP5)
irq = DigitalInOut(board.GP0)
rst = DigitalInOut(board.GP1)
bluefruit = BluefruitSPI(spi_bus, cs, irq, rst, debug=False)

# Initialize the device and perform a factory reset
print("Initializing the Bluefruit LE SPI Friend module")
bluefruit.init()
bluefruit.command_check_OK(b'AT+FACTORYRESET', delay=1)

# Print the response to 'ATI' (info request) as a string
print(str(bluefruit.command_check_OK(b'ATI'), 'utf-8'))

# Change advertised name
bluefruit.command_check_OK(b'AT+GAPDEVNAME=PicoBLE')

while True:
    print("Waiting for a connection to Bluefruit LE Connect ...")
    # Wait for a connection ...
    dotcount = 0
    while not bluefruit.connected:
        print(".", end="")
        dotcount = (dotcount + 1) % 80
        if dotcount == 79:
            print("")
        time.sleep(0.5)

    # Once connected, check for incoming BLE UART data
    print("\n *Connected!*")
    connection_timestamp = time.monotonic()
    while True:
        # Check our connection status every 3 seconds
        if time.monotonic() - connection_timestamp > 3:
            connection_timestamp = time.monotonic()
            if not bluefruit.connected:
                break

        # OK we're still connected, see if we have any data waiting
        resp = bluefruit.uart_rx()
        if not resp:
            continue  # nothin'
        print("Read %d bytes: %s" % (len(resp), resp))
        # Now write it!
        print("Writing reverse...")
        send = []
        for i in range(len(resp), 0, -1):
            send.append(resp[i-1])
        print(bytes(send))
        bluefruit.uart_tx(bytes(send))

    print("Connection lost.")
