import board
import busio
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import time

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

API_URL = "https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode={0}&date={1}&distance=25&API_KEY={2}"
API_KEY = secrets["api_key"]

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.GP7)
esp32_ready = DigitalInOut(board.GP10)
esp32_reset = DigitalInOut(board.GP11)

spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

zipcode = "14217"
date = ""
full_url = API_URL.format(zipcode, date, API_KEY)


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
            time.sleep(20)

    try:
        utc_time = esp.get_time()
    except Exception as e:
        print(e)
    else:
        date_obj = time.localtime(utc_time[0])
        date = str(date_obj.tm_year) + "-" + str(date_obj.tm_mon) + "-" + str(date_obj.tm_mday)
        full_url = API_URL.format(zipcode, date, API_KEY)

    try:
        response = requests.get(full_url)
    except Exception as e:
        print(e)
    else:
        data = response.json()[0]
        print("-" * 40)
        print("Reporting Area: ", data["ReportingArea"])
        print("AQI: ", data["AQI"])
        print("Category: ", data["Category"]["Name"])
        print("-" * 40)
        response.close()

    print("Done!")
    time.sleep(60)
