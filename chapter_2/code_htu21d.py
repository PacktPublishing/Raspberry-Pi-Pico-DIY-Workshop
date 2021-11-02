import time
import busio
import board
from adafruit_htu21d import HTU21D

i2c = busio.I2C(board.GP9, board.GP8)
sensor = HTU21D(i2c)

while True:
    print("\n Temperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(2)
