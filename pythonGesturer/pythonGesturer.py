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


# Global Variables
previousServoAngles = []
# Create a PySerial port with infinite timeout (blocks on reads), but not yet
# connected to a hardware port (read in from configs)
serialPort = serial.Serial(None, 9600, timeout = globalTimeout)
# Create a global timeout variable, so we can reset the timeout after performing
# a non-blocking read
globalTimeout = None

# Write an example updateGesture() to change the currentGesture value based on
# desired logic
def updateGesture():
    print "Unwritten, but shall update currentGesture based on user desired logic"


def gestureSmooth(sleepTime, numObjects, startPosArray, endPosArray):
    # Right now position arrays start as strings, so convert them to integers
    startPosArray = map(int, startPosArray)
    endPosArray = map(int, endPosArray)

    # Find the maximum distance between positions for the start and end positions
    # of each object
    maxDelta = 0
    for i in range(numObjects):
        testDelta = abs(startPosArray[i + 1] - endPosArray[i + 1])
        if maxDelta < testDelta:
            maxDelta = testDelta

    # Setup temporary buffer for transitionary positions
    servoValues = [0] * numObjects
    # Initialize the temporary buffer with the starting positions
    for i in range(numObjects):
        servoValues[i] = startPosArray[i + 1]

    # Linear smoothing over the range of the longest distance
    for i in range(maxDelta):
        # For each object
        for i in range(numObjects):
            # Linearly increment/decrement the servo value towards the end 
            # position value, how/if appropriate
            if servoValues[i] > endPosArray[i + 1]:
                servoValues[i] -= 1
            elif servoValues[i] < endPosArray[i + 1]:
                servoValues[i] += 1
            # Otherwise, the servo value is the end position value, and that 
            # servo stops animating

            print("Servo value is: " + str(servoValues[i]))
            # Write out the servo value to the Arduino and read back the return
            serialPort.write(struct.pack('B', servoValues[i]))
            serialRead = serialPort.read()

        # Sleep to create a frame rate
        time.sleep(sleepTime)       



def frame_handler(scene, numObjects, csvFile, motorIdentification):
    # Create an array to store the angles we get from the Blender scene, and a
    # bool to see if we should send these values to the Arduino
    newAngles = [0] * numObjects
    shouldResend = False

    # We will be modifying this global variable, so we declare it global
    global previousServoAngles

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(numObjects):
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
                # Make sure the value read by Arduino and returned is the same as 
                # that we sent, otherwise exit the program
                if ord(serialRead) != (181 + i):
                    sys.exit()
                    print("Serial send not equal to serial return")
                    break

            serialPort.write(struct.pack('B', newAngles[i]))
            # previousServoAngles[i] = newAngles[i]
            # print("Write angle " + str(i) + " is: " + str(newAngles[i]))

            serialRead = serialPort.read()
            # Make sure the value read by Arduino and returned is the same as 
            # that we sent, otherwise exit the program
            if ord(serialRead) != newAngles[i]:
                sys.exit()
                print("Serial send not equal to serial return")
                break
        shouldResend = False


def main():
    # We will be modifying this global variable, so we declare it global
    global previousServoAngles

    # Read in the YAML configs
    fileName = "gesturerConfigs.yaml"
    fileStream = open(fileName).read()

    switchNum = 400
    currentGesture = 0
    switchCount = 0

    configs = yaml.load(fileStream, Loader=yaml.Loader)
    # Load the YAML configs into global variables for easy access
    numObjects = configs["numObjects"]
    numGestures = configs["numGestures"]
    motorIdentification = configs["motorIdentification"]
    previousServoAngles = [0] * numObjects

    serialPort.port = configs["serialPort"]

    # TODO: Read in a single CSV file (name in the YAML). DONE
    # TODO: Calculate indexing into the CSV for each individual gesture, make
    # a dictionary/array to know how to index into the gestures
    # OR just read each gesture into a separate file! DONE (into separate arrays).

    csvOutputName = configs["csvOutputName"]

    # Read in the gesture csv files
    csvInputFile = open(csvOutputName, 'rt')
    reader = csv.reader(csvInputFile)
    row_count = 0
    csvGestureData = [[]] * numGestures
    csvGestureLength = [0] * numGestures

    # TODO: For each gesture, create a new entry in csvGestureData and populate
    # it with csv values (by appending). DONE
    gestureCount = 0
    # Read through the CSV file and populate the gesture data/length arrays 
    for row in reader:
        # If the first item in the CSV row is a "*", we have reached the end of
        # a gesture
        if row[0] == "*":
            csvGestureLength[gestureCount] = len(csvGestureData[gestureCount])
            gestureCount += 1
        # Otherwise, continue adding to the current gesture
        else:
            csvGestureData[gestureCount].append(row)

    # In case there was no "*" at the end of the last gesture, we set the last 
    # gesture length
    if gestureCount == (numGestures - 1):
        csvGestureLength[gestureCount] = len(csvGestureData[gestureCount])

    # Close the CSV input file
    csvInputFile.close()

    # Start the number of frames as the length of the currentGesture
    numFrames = csvGestureLength[currentGesture]

    serialPort.open()
    # Connecting time for Arduino
    time.sleep(3)

    # Set frame rate and corresponding sleep rate
    # TODO: import these from the YAML configs and have them be set by the user
    # to correspond with how the gesture was generated (in Blender or otherwise)
    frameRate = 24
    sleepTime = 1./frameRate

    # Main loop for executing gestures/the logic for switching between them
    # TODO: Add modular logic for switching between gestures. MOSTLY DONE (just 
    # need to write an example updateGesture())
    while True:

        for currentFrame in range(numFrames):
            # Read CSV data and send to Arduino if necessary
            frame_handler(currentFrame, numObjects, csvGestureData[currentGesture],  motorIdentification)
            # Sleep to create a frame rate
            time.sleep(sleepTime)
            
            # LOGIC FOR SWITCHING "currentGesture" GOES HERE

            # newGesture = updateGesture()

            # startPosArray = [0] * numObjects
            # endPosArray = [0] * numObjects
            # oldGesture = currentGesture
            # currentGesture = newGesture
            # startPosArray = csvGestureData[oldGesture][currentFrame]
            # endPosArray = csvGestureData[currentGesture][0]
            # numFrames = csvGestureLength[currentGesture]

            # Note, if you want linear smoothing between gestures, create arrays 
            # containing the start and end positions of each object and uncomment
            # the following line
            # gestureSmooth(sleepTime, numObjects, startPosArray, endPosArray)

            # BE SURE TO "break" AT THE END OF THE SWITCHING GESTURES LOGIC
            # break


if __name__ == "__main__":  
    main()  
