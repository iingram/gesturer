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

# Setup serial communication with Arduino
# Hardcoded for my current connection to the Arduino on my computer (Sky)

# Originally working without sending addressing value
# serialPort = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout = 0)
 
# Testing with infinite timeout, so blocking until it hears back from Arduino
# NOTE: This will most likely fail entirely, as we have been missing some bytes
#        occasionally on the Arduino side so we will probably not hear back after
#        some transmission
# ACTUALLY: This provides a nice check that our Serial communication is working
#            properly. If Serial fails, then all of Blender will lock up. This is
#            currently desired behavior but this is open for discussion!
serialPort = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout = None)

#serialPort = serial.Serial()


# Scene handler
# To be called any time there is a change within the scene (e.g. position change,
# rotation change, current frame change)
def my_handler(scene):
    # Want the YAML to include:
    #       - Name of the object
    #       - Arrtibute to watch (rotation x,y,z for now)
    #       - Number of data points to write out to serial (maybe a dictionary?)
    #       - Offset for the angle of each motor
    #       - 

    newAngles = [0] * GestureOperator.numObjects
    shouldResend = False

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(GestureOperator.numObjects):
        object = bpy.data.objects[GestureOperator.objectNames[i]]
        movement = degrees(object.rotation_euler[GestureOperator.objectAxes[i]])
        servoAngle = int(GestureOperator.objectOffsets[i] + movement)
        newAngles[i] = servoAngle


        #######################################################################
        # NOTE: having issues sending char values above 128 or so!!!!!! fixed!
        # Solution: issue was every time a larger char value was sent, we would 
        # get a byte of value 194 before the return, so we just read away that 
        # byte if it exists
        #
        # DANGER DANGER: This is a temporary fix, we need to find out what is 
        # really going on
        # HALLELUJAH! Using struct.pack to create actual bytes rather than using
        # chars was the key!!! Avoid chr() from now on.

        # If the angle of a motor has changed, rewrite them all to Arduino
        if (servoAngle != GestureOperator.previousServoAngles[i]):
            shouldResend = True

    if (shouldResend == True):
        for i in range(GestureOperator.numObjects):
            #serialPort.write(newAngles[i].encode())
            serialPort.write(struct.pack('B', newAngles[i]))
            GestureOperator.previousServoAngles[i] = newAngles[i]
            print("Write angle " + str(i) + " is: " + str(newAngles[i]))

            serialInput = serialPort.read()
            # If we receive a value of 194, this *was* an odd error due to sending
            # a value larger than 128, but won't work for our Servos so we ignore it
            #
            # Most likely get rid of this as we now do not have this issue because
            # we are creating bytes with struct.pack not chr()
            if (ord(serialInput) == 194):
                print("Read bad char: " + str(ord(serialInput)))
                serialInput = serialPort.read()
            print("Read angle " + str(i) + " is: " + str(ord(serialInput)))

            if (ord(serialInput) != newAngles[i]):
                stop_operator()
                print("Serial input not equal to serial output")
                break
        shouldResend = False

    # non_blocking_read()
   

# GestureOperator class
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

    # Boolean to see if the scene handler should be set or reset
    isHandling = False
    # Boolean to see if we should load in configuration data
    loadConfigs = True
  
    # Run on execution of the "Gesture Operator"
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
            GestureOperator.previousServoAngles = [0] * GestureOperator.numObjects
            # Currently, only load the configs when the "Gesture Operator" 
            # is first called
            GestureOperator.loadConfigs = False

        # If we are not currently handling scene changes, set function "my_handler"
        # to be run every scene change
        if GestureOperator.isHandling == False:  
            bpy.app.handlers.scene_update_pre.append(my_handler)
            GestureOperator.isHandling = True
        # If we were handling scene changes, remove our handler from the handler list
        # by reverse enumerating and popping it off
        else:
            myHandlerList = bpy.app.handlers.scene_update_pre
            numHandlers = len(myHandlerList)
            for handlerID, function in enumerate(reversed(myHandlerList)):
                if function.__name__ == 'my_handler':
                    myHandlerList.pop(numHandlers - 1 - handlerID)
            GestureOperator.isHandling = False
        # Blender Python internals, must return {'FINISHED'}
        return {'FINISHED'}
      


def non_blocking_read():
    serialPort.timeout = 0
    serialInput = serialPort.read()
    serialPort.timeout = None

    if (len(serialInput) > 0):
        print("Non-blocking read received: " + str(ord(serialInput)))
        return serialInput

    return None


def stop_operator():
    myHandlerList = bpy.app.handlers.scene_update_pre
    numHandlers = len(myHandlerList)
    for handlerID, function in enumerate(reversed(myHandlerList)):
        if function.__name__ == 'my_handler':
            myHandlerList.pop(numHandlers - 1 - handlerID)
    GestureOperator.isHandling = False


# Register the GestureOperator class with Blender  
def register():  
    bpy.utils.register_class(GestureOperator) 
    # Add the button for activating the "Gesture Operator" to the 3d View

# For testing purposes, so the script will register the class when called directly
if __name__ == "__main__":  
    register()  