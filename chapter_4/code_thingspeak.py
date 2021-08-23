# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import busio
import neopixel
from adafruit_seesaw.seesaw import Seesaw
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

i2c = busio.I2C(board.GP9, board.GP8)

ss = Seesaw(i2c, addr=0x36)

pixel_pin = board.GP0

num_pixels = 1

ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

esp32_cs = DigitalInOut(board.GP7)
esp32_ready = DigitalInOut(board.GP10)
esp32_reset = DigitalInOut(board.GP11)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue

print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

while True:
    # read moisture level
    touch = ss.moisture_read()

    # read temperature from the temperature sensor
    temp = ss.get_temp()

    print("temp: " + str(temp) + "  moisture: " + str(touch))

    if touch > 500:
        pixels.fill((0, 0, 255, 0))
        pixels.show()
        time.sleep(0.250)
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(0.250)
        print()
        r = requests.get("https://api.thingspeak.com/update?api_key=ABCDEFGHIJKL&field1=" + str(touch))
        print("-" * 40)
        print(r.json())
        print("-" * 40)
        r.close()
        print("Done!")
    time.sleep(2)
