import time
import board
import analogio

vane = analogio.AnalogIn(board.A1)

def get_voltage(raw):
    return (raw * 3.3) / 65536

def wind_dir(vin):
    if vin < 150: windDir="202.5"
    elif vin < 300: windDir = "180"
    elif vin < 400: windDir = "247.5"
    elif vin < 600: windDir = "225"
    elif vin < 900: windDir = "292.5"
    elif vin < 1100: windDir = "270"
    elif vin < 1500: windDir = "112.5"
    elif vin < 1700: windDir = "135"
    elif vin < 2250: windDir = "337.5"
    elif vin < 2350: windDir = "315"
    elif vin < 2700: windDir = "67.5"
    elif vin < 3000: windDir = "90"
    elif vin < 3200: windDir = "22.5"
    elif vin < 3400: windDir = "45"
    elif vin < 4000: windDir = "0"
    else: windDir = "0"

    return windDir


while True:
    raw = vane.value
    volts = get_voltage(raw)
    print("raw = {:5d} volts = {:5.2f} angle={}".format(raw, volts, wind_dir(volts * 1000)))
    time.sleep(0.5)
