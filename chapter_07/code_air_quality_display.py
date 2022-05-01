import board
import busio
import digitalio
import time
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_motor import stepper

DELAY = 0.01
STEPS = 400

coils = (
    digitalio.DigitalInOut(board.GP12),  # A1
    digitalio.DigitalInOut(board.GP13),  # A2
    digitalio.DigitalInOut(board.GP14),  # B1
    digitalio.DigitalInOut(board.GP15),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

# step count for display
position = [75, 125, 175, 225, 275, 325]
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

API_URL = "https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode={0}&date={1}&distance=25&API_KEY={2}"
API_KEY = secrets["api_key"]

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = digitalio.DigitalInOut(board.GP7)
esp32_ready = digitalio.DigitalInOut(board.GP10)
esp32_reset = digitalio.DigitalInOut(board.GP11)

spi = busio.SPI(board.GP18, board.GP19, board.GP16)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
requests.set_socket(socket, esp)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue

print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

zipcode = input("Enter a valid 5-digit zipcode: ")
date = input("Enter today's date in the following format YYYY-MM-DD: ")

full_url = API_URL.format(zipcode, date, API_KEY)

try:
    response = requests.get(full_url)
except Exception as e:
    print(e)
else:
    print("Homing...")
    for step in range(STEPS):
        motor.onestep()
        time.sleep(DELAY)

    data = response.json()[0]
    print("-" * 40)
    print("Reporting Area: ", data["ReportingArea"])
    print("AQI: ", data["AQI"])
    print("Category: ", data["Category"]["Name"])
    index = int(data["Category"]["Number"])
    print(index)
    for step in range(position[index - 1]):
        motor.onestep(direction=stepper.BACKWARD)
        time.sleep(DELAY)
    print("-" * 40)
    response.close()

print("Done!")
