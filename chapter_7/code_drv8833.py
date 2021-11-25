import time
import board
import digitalio
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

for step in range(STEPS):
    motor.onestep()
    time.sleep(DELAY)

for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD)
    time.sleep(DELAY)

motor.release()
