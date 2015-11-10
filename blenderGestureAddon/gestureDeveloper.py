# gestureDeveloper.py
# Created by Skyler Williams
#
# Blender plugin to help develop gestures for robotics. 
# 

import bpy
import serial
import yaml
import os
import struct
from time import sleep
from math import degrees

# Blender Addon internals, information about the addon
bl_info = {  
 "name": "Gesture Operator",  
 "author": "Skyler Williams",  
 "version": (1, 0),  
 "blender": (2, 6, 4),  
 "location": "View3D > Object > Gesture Operator",  
 "description": "Starts the gesture communication for robotics",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Object"} 
 
# Create a global timeout variable, so we can reset the timeout after performing
# a non-blocking read
globalTimeout = None


# Create a PySerial port with infinite timeout (blocks on reads), but not yet
# connected to a hardware port (read in from configs)
serialPort = serial.Serial(None, 9600, timeout = globalTimeout)

# gesture_handler(scene)
#
# To be called any time there is a change within the scene (e.g. position change,
# rotation change, current frame change)
def gesture_handler(scene):
    # Want the YAML to include:
    #       - Name of the object
    #       - Arrtibute to watch (rotation x,y,z for now)
    #       - Number of data points to write out to serial (maybe a dictionary?)
    #       - Offset for the angle of each motor
    #       - Addressing scheme for motors
    #       - Serial port to connect through

    # Create an array to store the angles we get from the Blender scene, and a
    # bool to see if we should send these values to the Arduino
    newAngles = [0] * GestureOperator.numObjects
    shouldResend = False

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(GestureOperator.numObjects):
        object = bpy.data.objects[GestureOperator.objectNames[i]]
        movement = degrees(object.rotation_euler[GestureOperator.objectAxes[i]])
        servoAngle = int(GestureOperator.objectOffsets[i] + movement)
        newAngles[i] = servoAngle

        # If the angle of a motor has changed, rewrite them all to Arduino
        if (servoAngle != GestureOperator.previousServoAngles[i]):
            shouldResend = True
            GestureOperator.previousServoAngles[i] = newAngles[i]

    # If we should resend the motor positons, loop through and send each based
    # on the motor identification scheme (addressing/switching)
    if (shouldResend == True):
        for i in range(GestureOperator.numObjects):
            # If we are addressing motors, first send "i"
            if (GestureOperator.motorIdentification == "addressing"):
                serialPort.write(struct.pack('B', i))
                serialRead = serialPort.read()
                # NOTE:
                # Need to check if it's a chr or "string of length 0" before
                # we print to stop getting that error and to see what's going on
                print("Address is: " + str(ord(serialRead)))
                if (ord(serialRead) != i):
                    stop_operator()
                    print("Serial send not equal to serial return")
                    break

            serialPort.write(struct.pack('B', newAngles[i]))
            # GestureOperator.previousServoAngles[i] = newAngles[i]
            print("Write angle " + str(i) + " is: " + str(newAngles[i]))

            serialRead = serialPort.read()
            # NOTE:
            # Need to check if it's a chr or "string of length 0" before
            # we print to stop getting that error and to see what's going on
            print("Read angle " + str(i) + " is: " + str(ord(serialRead)))
            if (ord(serialRead) != newAngles[i]):
                stop_operator()
                print("Serial send not equal to serial return")
                break
        shouldResend = False
   

# GestureOperator class
#
# Blender Addons are implemented via Python classes, so we create a class here
# and populate it with the desired logic in the methods required by Blender.
#
class GestureOperator(bpy.types.Operator): 
    # Blender Addon internals 
    bl_idname = "object.gesture_operator"  
    bl_label = "Gesture Operator"  
    
    # Raw configuration data
    configs = {}
    # Extracted configuration data
    numObjects = 0
    objectNames = []
    objectAxes = []
    objectOffsets = []
    previousServoAngles = []
    motorIdentification = ""

    # Boolean to see if the scene handler should be set or reset
    isHandling = False
    # Boolean to see if we should load in configuration data
    loadConfigs = True
    
    # execute(self, context)
    #
    # Run on execution of the "Gesture Operator". Required function.
    def execute(self, context):
        # Check if we should load the configs (and do so if necessary)
        if GestureOperator.loadConfigs == True:
            fileName = os.path.join(os.path.dirname(bpy.data.filepath), "gesturerConfigs.yaml")
            fileStream = open(fileName).read()
            GestureOperator.configs = yaml.load(fileStream, Loader=yaml.Loader)

            GestureOperator.objectNames = GestureOperator.configs["objectNames"]
            GestureOperator.objectAxes = GestureOperator.configs["objectAxes"]
            GestureOperator.objectOffsets = GestureOperator.configs["objectOffsets"]
            GestureOperator.numObjects = GestureOperator.configs["numObjects"]
            GestureOperator.motorIdentification = GestureOperator.configs["motorIdentification"]
            GestureOperator.previousServoAngles = [0] * GestureOperator.numObjects
            serialPort.port = GestureOperator.configs["serialPort"]
            # Currently, only load the configs when the "Gesture Operator" 
            # is first called
            GestureOperator.loadConfigs = False

        # If we are not currently handling scene changes, set function "gesture_handler"
        # to be run every scene change
        if GestureOperator.isHandling == False: 
            # NOTE: This takes a moment to actually open, so we want to wait until
            #   we know it's open to add our handler to the scene update. Need to
            #   find a better way than hardcoding a sleep value, but it works for now 
            serialPort.open()
            print("Opening Serial port, waiting for 2 seconds to connect...")
            sleep(2)
            bpy.app.handlers.scene_update_pre.append(gesture_handler)
            GestureOperator.isHandling = True
        # If we were handling scene changes, remove our handler from the handler list
        # by reverse enumerating and popping it off
        else:
            stop_operator()
        # Blender Python internals, must return {'FINISHED'}
        return {'FINISHED'}
      

# non_blocking_read()
# 
# Performs a non-blocking read on the global serialPort by setting the timeout
# to 0, reading, and then setting the timeout back to the globalTimeout value.
def non_blocking_read():
    serialPort.timeout = 0
    serialRead = serialPort.read()
    serialPort.timeout = globalTimeout

    if (len(serialRead) > 0):
        print("Non-blocking read received: " + str(ord(serialRead)))
        return serialRead

    return None


# stop_operator()
#
# Stops the function of the addon by removing the scene handler we added to 
# capture and send object positions, and by closing the serial port. 
def stop_operator():
    myHandlerList = bpy.app.handlers.scene_update_pre
    numHandlers = len(myHandlerList)
    for handlerID, function in enumerate(reversed(myHandlerList)):
        if function.__name__ == 'gesture_handler':
            myHandlerList.pop(numHandlers - 1 - handlerID)
    serialPort.close()
    GestureOperator.isHandling = False

# register()
#
# Registers the GestureOperator class with Blender. Required function. 
def register():  
    bpy.utils.register_class(GestureOperator) 
    # Add the button for activating the "Gesture Operator" to the 3d View

# For testing purposes, so the script will register the class when called directly
if __name__ == "__main__":  
    register()  