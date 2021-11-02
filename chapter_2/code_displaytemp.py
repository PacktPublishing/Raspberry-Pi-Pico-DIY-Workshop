import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_htu21d import HTU21D


displayio.release_displays()

oled_reset = board.GP12

# Use for SPI
spi = busio.SPI(board.GP2, MOSI=board.GP3)
i2c = busio.I2C(board.GP9, board.GP8)

oled_cs = board.GP11
oled_dc = board.GP13
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs,
                                reset=oled_reset, baudrate=1000000)

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed

sensor = HTU21D(i2c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

while True:
    splash = displayio.Group()

    text = "Temperature: {:.1f} C".format(sensor.temperature)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=4)
    splash.append(text_area)
    display.show(splash)

    text = "Humidity: {:.1f} %".format(sensor.relative_humidity)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=17)
    splash.append(text_area)
    display.show(splash)

    time.sleep(2)




