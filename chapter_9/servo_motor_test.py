from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()

while True:
    buggy.goToPosition(2,180)
    sleep(5)
    buggy.goToPosition(2,0)
    sleep(5)