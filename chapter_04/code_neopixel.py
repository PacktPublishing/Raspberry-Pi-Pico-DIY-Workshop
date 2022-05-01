# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import busio
import neopixel
from adafruit_seesaw.seesaw import Seesaw

i2c = busio.I2C(board.GP9, board.GP8)

ss = Seesaw(i2c, addr=0x36)

pixel_pin = board.GP0

num_pixels = 1

ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

while True:
    # read moisture level
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    print("temp: " + str(temp) + "  moisture: " + str(touch))

    if touch < 500:
        pixels.fill((0, 0, 255, 0))
        pixels.show()
        time.sleep(0.250)
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(0.250)
