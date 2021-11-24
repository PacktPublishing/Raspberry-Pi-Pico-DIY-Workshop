import time
import board
import busio
import adafruit_scd30

i2c = busio.I2C(board.GP9, board.GP8)
scd = adafruit_scd30.SCD30(i2c)

while True:
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)

    time.sleep(2.0)
