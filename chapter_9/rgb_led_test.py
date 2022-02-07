#rotates colours on ZIP LEDs when the button is pressed

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

my_robot = KitronikPicoRobotBuggy()
LEDState = 0

def LEDPattern():
    global LEDState
    
    if LEDState == 0:
        my_robot.setLED(3,my_robot.BLUE)
        my_robot.setLED(0,my_robot.GREEN)
        my_robot.setLED(1,my_robot.YELLOW)
        my_robot.setLED(2,my_robot.RED)
        LEDState = 1
    elif LEDState == 1:
        my_robot.setLED(2,my_robot.BLUE)
        my_robot.setLED(3,my_robot.GREEN)
        my_robot.setLED(0,my_robot.YELLOW)
        my_robot.setLED(1,my_robot.RED)
        LEDState = 2
    elif LEDState == 2:
        my_robot.setLED(1,my_robot.BLUE)
        my_robot.setLED(2,my_robot.GREEN)
        my_robot.setLED(3,my_robot.YELLOW)
        my_robot.setLED(0,my_robot.RED)
        LEDState = 3
    elif LEDState == 3:
        my_robot.setLED(0,my_robot.BLUE)
        my_robot.setLED(1,my_robot.GREEN)
        my_robot.setLED(2,my_robot.YELLOW)
        my_robot.setLED(3,my_robot.RED)
        LEDState = 4
    else:
        my_robot.setLED(0,my_robot.BLACK)
        my_robot.setLED(1,my_robot.BLACK)
        my_robot.setLED(2,my_robot.BLACK)
        my_robot.setLED(3,my_robot.BLACK)
        LEDState = 0
    my_robot.show()



while True:
    LEDPattern()
    sleep(1)
