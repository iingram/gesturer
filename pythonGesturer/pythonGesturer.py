# pythonGesturer.py
# Created by Skyler Williams
#
# Python script for communicating gestural animation data to an Arduino from
# CSV files.
# 

import csv
import os
import serial
import sys
import time
import yaml



# Create a global timeout variable, so we can reset the timeout after performing
# a non-blocking read
globalTimeout = None


csv1f = open("animationOutput.csv", 'rt')
reader = csv.reader(csv1f)
row_count = sum(1 for row in reader)
csv1Reader = [""] * row_count


numFrames = len(csv1Reader)

configs = ""
numObjects = 0
motorIdentification = ""
previousServoAngles = []


# Create a PySerial port with infinite timeout (blocks on reads), but not yet
# connected to a hardware port (read in from configs)
serialPort = serial.Serial(None, 9600, timeout = globalTimeout)





def frame_handler(scene):
    # Create an array to store the angles we get from the Blender scene, and a
    # bool to see if we should send these values to the Arduino
    newAngles = [0] * numObjects
    shouldResend = False

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(numObjects):
        # TODO: Replace this with reading CSV logic to get newAngles correctly
        servoAngle = int(csv1Reader[scene][i])
        newAngles[i] = servoAngle

        # If the angle of a motor has changed, rewrite them all to Arduino
        if (servoAngle != previousServoAngles[i]):
            shouldResend = True
            previousServoAngles[i] = newAngles[i]

    # If we should resend the motor positons, loop through and send each based
    # on the motor identification scheme (addressing/switching)
    if (shouldResend == True):
        for i in range(numObjects):
            # If we are addressing motors, first send "i"
            if (motorIdentification == "addressing"):
                serialPort.write(struct.pack('B', (181 + i)))
                serialRead = serialPort.read()
                # NOTE:
                # Need to check if it's a chr or "string of length 0" before
                # we print to stop getting that error and to see what's going on
                print("Address is: " + str(ord(serialRead)))
                if (ord(serialRead) != (181 + i)):
                    sys.exit()
                    print("Serial send not equal to serial return")
                    break

            serialPort.write(struct.pack('B', newAngles[i]))
            # previousServoAngles[i] = newAngles[i]
            print("Write angle " + str(i) + " is: " + str(newAngles[i]))

            serialRead = serialPort.read()
            # NOTE:
            # Need to check if it's a chr or "string of length 0" before
            # we print to stop getting that error and to see what's going on
            print("Read angle " + str(i) + " is: " + str(ord(serialRead)))
            if (ord(serialRead) != newAngles[i]):
                sys.exit()
                print("Serial send not equal to serial return")
                break
        shouldResend = False




def main():
    # Read in the YAML configs
    fileName = "gesturerConfigs.yaml"
    fileStream = open(fileName).read()
    configs = yaml.load(fileStream, Loader=yaml.Loader)
    # Load the YAML configs into global variables for easy access
    numObjects = configs["numObjects"]
    motorIdentification = configs["motorIdentification"]
    previousServoAngles = [0] * numObjects
    serialPort.port = configs["serialPort"]


    frameRate = 24
    sleepTime = 1./frameRate

    while True:
        for i in range(numFrames):
            # Read CSV data and send to Arduino if necessary
            frame_handler(i)
            print("Frame " + str(i))
            # Sleep to create a frame rate
            time.sleep(sleepTime)
            # TODO: Twitter checks in another thread? Change the CSV to read from,
            # then set something that after some period of time changes back to the
            # original CSV gesture




if __name__ == "__main__":  
    main()  
