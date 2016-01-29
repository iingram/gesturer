# pythonGesturer.py
# Created by Skyler Williams
#
# Python script for communicating gestural animation data to an Arduino from
# CSV files.
# 

import csv
import serial
import struct
import sys
import time
import yaml


# Create a global timeout variable, so we can reset the timeout after performing
# a non-blocking read
globalTimeout = None


previousServoAngles = []


# Create a PySerial port with infinite timeout (blocks on reads), but not yet
# connected to a hardware port (read in from configs)
serialPort = serial.Serial(None, 9600, timeout = globalTimeout)

def frame_handler(scene, numObjects, csvFile, motorIdentification):
    # Create an array to store the angles we get from the Blender scene, and a
    # bool to see if we should send these values to the Arduino
    newAngles = [0] * numObjects
    shouldResend = False

    global previousServoAngles

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(numObjects):
        # TODO: Replace this with reading CSV logic to get newAngles correctly
        # We index plus 1 into the csvFile since there is timestep data
        servoAngle = int(csvFile[scene][i + 1])
        if (servoAngle > 180):
            servoAngle = 180
        elif (servoAngle < 0):
            servoAngle = 0
        newAngles[i] = servoAngle
        # print("Servo " + str(i) + "is: " + str(servoAngle))

        # If the angle of a motor has changed, rewrite them all to Arduino
        if servoAngle != previousServoAngles[i]:
            shouldResend = True

            previousServoAngles[i] = newAngles[i]

    # If we should resend the motor positons, loop through and send each based
    # on the motor identification scheme (addressing/switching)
    if shouldResend == True:
        for i in range(numObjects):
            # If we are addressing motors, first send "i"
            if motorIdentification == "addressing":
                serialPort.write(struct.pack('B', (181 + i)))
                serialRead = serialPort.read()
                # NOTE:
                # Need to check if it's a chr or "string of length 0" before
                # we print to stop getting that error and to see what's going on
                # print("Address is: " + str(ord(serialRead)))
                if ord(serialRead) != (181 + i):
                    sys.exit()
                    print("Serial send not equal to serial return")
                    break

            serialPort.write(struct.pack('B', newAngles[i]))
            # previousServoAngles[i] = newAngles[i]
            # print("Write angle " + str(i) + " is: " + str(newAngles[i]))

            serialRead = serialPort.read()
            # NOTE:
            # Need to check if it's a chr or "string of length 0" before
            # we print to stop getting that error and to see what's going on
            # print("Read angle " + str(i) + " is: " + str(ord(serialRead)))
            if ord(serialRead) != newAngles[i]:
                sys.exit()
                print("Serial send not equal to serial return")
                break
        shouldResend = False


def main():
    # Read in the YAML configs
    fileName = "gesturerConfigs.yaml"
    fileStream = open(fileName).read()

    # Read in the gesture csv files
    csv0 = open("animationOutput0.csv", 'rt')
    reader = csv.reader(csv0)
    row_count = 0
    csvFile0 = []
    for row in reader:
        csvFile0.append(row)
        row_count += 1
        print row
    csvLen0 = len(csvFile0)

    numFrames = csvLen0

    print(numFrames)

    configs = ""
    numObjects = 0
    motorIdentification = ""
 
    global tweetURL
    global previousServoAngles
    global serialPort
    configs = yaml.load(fileStream, Loader=yaml.Loader)
    # Load the YAML configs into global variables for easy access
    numObjects = configs["numObjects"]
    motorIdentification = configs["motorIdentification"]
    previousServoAngles = [0] * numObjects

    serialPort.port = configs["serialPort"]
    serialPort.open()
    # Connecting time for Arduino
    time.sleep(3)

    frameRate = 24
    sleepTime = 1./frameRate

    while True:

        for i in range(numFrames):
            # Read CSV data and send to Arduino if necessary
            frame_handler(i, numObjects, csvFile0,  motorIdentification)
            #print("Frame " + str(i))
            # Sleep to create a frame rate
            time.sleep(sleepTime)

        numFrames = csvLen0




if __name__ == "__main__":  
    main()  
