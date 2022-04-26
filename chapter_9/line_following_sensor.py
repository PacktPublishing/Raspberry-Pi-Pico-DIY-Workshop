from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep
buggy = KitronikPicoRobotBuggy()

while True:
    print ("L" , buggy.getRawLFValue("l"), " R", buggy.getRawLFValue("r"), " C",buggy.getRawLFValue("c"))
    sleep(1)