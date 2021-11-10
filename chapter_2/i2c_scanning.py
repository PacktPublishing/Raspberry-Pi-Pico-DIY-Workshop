import time
import board
import busio

i2c = busio.I2C(board.GP9, board.GP8)

while not i2c.try_lock():
    pass

try:
    while True:
        print("I2C addresses found:", [hex(device_address)
              for device_address in i2c.scan()])
        time.sleep(2)

finally:
    i2c.unlock()
