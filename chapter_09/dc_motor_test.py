#changes motors in sequence based on user buton pressing

from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from time import sleep

buggy = KitronikPicoRobotBuggy()
state = 0

def MotorControl():
    global state
    
    if state == 0:
        print("Moving Forward...")
        buggy.motorOn("l","f",100)
        buggy.motorOn("r","f",100)
        state = 1
    elif state == 1:
        print("Moving Backward...")
        buggy.motorOn("l","r",100)
        buggy.motorOn("r","r",100)
        state = 2
    else:
        print("Turning Off...")
        buggy.motorOff("l")
        buggy.motorOff("r")
        state = 0
            

while True:
    MotorControl()
    sleep(10)

