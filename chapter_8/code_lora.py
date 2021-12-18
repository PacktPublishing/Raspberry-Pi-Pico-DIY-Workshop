# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of sending and recieving data with the RFM95 LoRa radio.
# Author: Tony DiCola
import board
import busio
import digitalio
import adafruit_rfm9x

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0

CS = digitalio.DigitalInOut(board.GP5)
RESET = digitalio.DigitalInOut(board.GP6)

LED = digitalio.DigitalInOut(board.GP25)
LED.direction = digitalio.Direction.OUTPUT

spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x.tx_power = 23


rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
print("Sent Hello World message!")


print("Waiting for packets...")

while True:
    rfm9x.send(bytes("Hello world!\r\n", "utf-8"))
    packet = rfm9x.receive()

    if packet is None:
        LED.value = False
        print("Received nothing! Listening again...")
    else:
        LED.value = True
        print("Received (raw bytes): {0}".format(packet))

        packet_text = str(packet, "ascii")
        print("Received (ASCII): {0}".format(packet_text))

        rssi = rfm9x.last_rssi
        print("Received signal strength: {0} dB".format(rssi))