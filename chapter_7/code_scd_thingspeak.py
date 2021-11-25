import board
import busio
import time
import adafruit_scd30
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

API_URL = "https://api.thingspeak.com/update?api_key={0}&field1={1}"
API_KEY = secrets["api_key"]

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.GP7)
esp32_ready = DigitalInOut(board.GP10)
esp32_reset = DigitalInOut(board.GP11)

spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

i2c = busio.I2C(board.GP9, board.GP8)
scd = adafruit_scd30.SCD30(i2c)

while True:
    while not esp.is_connected:
        try:
            print("Connecting to AP...")
            esp.connect_AP(secrets["ssid"], secrets["password"])
        except RuntimeError as e:
            print("could not connect to AP, retrying: ", e)
            continue
        else:
            print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
            print("My IP address is", esp.pretty_ip(esp.ip_address))

    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        full_url = API_URL.format(API_KEY)

        try:
            response = requests.get(full_url)
        except Exception as e:
            print(e)
        else:
            print("-" * 40)
            print(response.json())
            print("-" * 40)
            response.close()
            print("Done!")
    time.sleep(20)
