import time
import board
import busio
import adafruit_ahtx0

# Create sensor object, communicating over the board's default I2C bus
i2c = busio.I2C(board.GP9, board.GP8)
sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    time.sleep(2)
