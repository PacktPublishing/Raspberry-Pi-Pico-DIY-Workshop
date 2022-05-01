from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()

while True:
    print("Closing...")
    buggy.goToPosition(2,180)
    sleep(5)
    print("Retracting...")
    buggy.goToPosition(2,0)
    sleep(5)

