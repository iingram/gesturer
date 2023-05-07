"""Addon for Blender to control robot over TCP/IP socket connection.

Allows the creation of a repertoire of gestures/behaviors that the
robots can then use in their activities.

"""

import math
import time
import os
import sys
import inspect
import socket
import struct
from threading import Thread

import yaml
import bpy

servo_angles = [0]


class RobotSocketHandler(Thread):
    """Handles connection to robot

    """

    def __init__(self,
                 num_servos,
                 server_address,
                 servo_angles):
        super().__init__()

        self.servo_angles = servo_angles

        self.sig = 'I' * num_servos

        sock = socket.socket()
        print('[INFO] Robot Server IP and Port: {}'.format(server_address))
        sock.connect(server_address)
        print('[INFO] Socket connection successful')
        self.stream = sock.makefile('wb')

    def run(self):
        try:
            while True:
                to_send = struct.pack(self.sig, *self.servo_angles)
                self.stream.write(to_send)
                self.stream.flush()
                time.sleep(0.03)
        except Exception as e:
            print(type(e))
            print(e)
            self.stream.close()


# File name
filename = inspect.getfile(inspect.currentframe())
print('Filename is {}'.format(filename))
# Path to file
path_to_file = os.path.dirname(os.path.abspath(filename))
print('Path to file is {}'.format(path_to_file))

sys.path.append(path_to_file)

# Blender Addon internals, information about the addon
bl_info = {
 "name": "Gesture Operator",
 "author": "Skyler Williams and Ian Ingram",
 "version": (1, 0, 1),
 "blender": (2, 6, 4),
 "location": "View3D > Object > Gesture Operator",
 "description": "Starts the gesture communication for robotics",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
 "category": "Object"}

# Create a global timeout variable, so we can reset the timeout after
# performing a non-blocking read
globalTimeout = None


# To be called any time there is a change within the scene
# (e.g. position change, rotation change, current frame change)
def gesture_handler(scene):
    global csvOutput
    global servo_angles

    determine_current_gesture(scene.frame_current)

    # Only handle the scene if it is within a gesture
    if GestureOperator.current_gesture != -1:
        # Create an array to store the angles we get from the Blender
        # scene, and a bool to see if we should send these values to
        # the Arduino
        newAngles = [0] * GestureOperator.numObjects
        # shouldResend = False

        # Create the base for the CSV output for each servo (aka each Object)
        # Will exist even for frames with no gesture, to make indexing into
        # the CSV from the YAML start/end values easier
        num_objects = GestureOperator.numObjects
        GestureOperator.csvOutput[scene.frame_current] = [0] * num_objects

        # Generalized loop for putting an arbitrary number of object
        # parameters out on the socket connection
        for i in range(GestureOperator.numObjects):
            # select the object by its name
            object = bpy.data.objects[GestureOperator.objectNames[i]]
            # determine which axis is animated for that object
            animated_axis = GestureOperator.objectAxes[i]
            # calculate the current angle in degrees of that object
            angle_deg = int(math.degrees(object.rotation_euler[animated_axis]))
            # NOTE: should the multipliers really be converted to int this way?
            servoAngle = (int(GestureOperator.offsets[i])
                          + int(GestureOperator.multipliers[i]) * angle_deg)
            if servoAngle <= 0:
                servoAngle = 0
            elif servoAngle >= 180:
                servoAngle = 180

            newAngles[i] = servoAngle

            # Set the CSV output for the given servo and angle
            GestureOperator.csvOutput[scene.frame_current][i] = servoAngle

            # If the angle of a motor has changed, rewrite them all to Arduino
            if servoAngle != GestureOperator.previousServoAngles[i]:
                # shouldResend = True
                GestureOperator.previousServoAngles[i] = newAngles[i]

        temp = [int(angle) for angle in newAngles]
        for i in range(len(servo_angles)):
            servo_angles[i] = temp[i]

        # for i in range(GestureOperator.numObjects):

            # servo_angle = int(newAngles[i])
            # if (servo_angle > 180):
            #     servo_angle = 180
            # elif (servo_angle < 0):
            #     servo_angle = 0
            # servo_angles[i] = servo_angle

        #   print("Write angle " + str(i) + " is: " + str(newAngles[i]))

    # If we are not within a gesture, tell the user
    else:
        print("Frame " + str(scene.frame_current) + " is not within a gesture")


class GestureOperator(bpy.types.Operator):
    """Defines the custom Blender Add-On

    Blender Addons are implemented via Python classes, so we create a
    class and populate it with the desired logic in the methods
    required by Blender.

    """
    bl_idname = "object.gesture_operator"
    bl_label = "Gesture Operator"

    # Extracted configuration data
    numObjects = 0
    objectNames = []
    objectAxes = []
    offsets = []
    multipliers = []
    previousServoAngles = []
    numGestures = 0
    gestureFrames = []
    csvOutputName = ""
    shouldOutputCSV = False
    gestureDelimiter = ""
    # Create a dictionary of values to be written out to CSVs
    csvOutput = {}

    current_gesture = -1

    # Boolean to see if the scene handler should be set or reset
    isHandling = False
    # Boolean to see if we should load in configuration data
    loadConfigs = True

    # execute(self, context)
    #
    # Run on execution of the "Gesture Operator". Required function.
    def execute(self, context):
        global servo_angles

        # Check if we should load the configs (and do so if necessary)
        if GestureOperator.loadConfigs:
            print('[INFO] Loading Configurations')

            fileName = os.path.join(os.path.dirname(bpy.data.filepath),
                                    "gesturer_configs.yaml")
            fileStream = open(fileName).read()
            configs = yaml.load(fileStream, Loader=yaml.Loader)

            # TODO: Put all of this within a try catch and catch
            # KeyErrors for improperly constructed YAML files
            GestureOperator.ip = configs["robot_ip"]
            GestureOperator.port = int(configs["robot_port"])

            GestureOperator.objectNames = configs["objectNames"]
            GestureOperator.objectAxes = configs["objectAxes"]
            GestureOperator.offsets = configs["objectOffsets"]
            GestureOperator.multipliers = configs["objectMultipliers"]
            GestureOperator.numObjects = configs["numObjects"]
            GestureOperator.previousServoAngles = [0] * configs["numObjects"]
            GestureOperator.numGestures = configs["numGestures"]
            GestureOperator.gestureFrames = configs["gestureFrames"]
            GestureOperator.csvOutputName = configs["csvOutputName"]
            GestureOperator.shouldOutputCSV = configs["shouldOutputCSV"]
            GestureOperator.gestureDelimiter = configs["gestureDelimiter"]
            # Currently, only load the configs when the "Gesture
            # Operator" is first called
            GestureOperator.loadConfigs = False

            # do this only the first time the operator is turned on
            if len(servo_angles) != GestureOperator.numObjects:
                for i in range(GestureOperator.numObjects - 1):
                    servo_angles.append(0)

        # If we are not currently handling scene changes, set function
        # "gesture_handler" to be run every scene change
        if not GestureOperator.isHandling:
            # NOTE: This takes a moment to actually open, so we want
            #   to wait until we know it's open to add our handler to
            #   the scene update. Need to find a better way than
            #   hardcoding a sleep value, but it works for now
            print('[INFO] Starting servo socket handler')
            servo_commander = RobotSocketHandler(GestureOperator.numObjects,
                                                 (GestureOperator.ip,
                                                  GestureOperator.port),
                                                 servo_angles)
            servo_commander.setDaemon(True)
            servo_commander.start()

            # time.sleep(1)
            bpy.app.handlers.scene_update_pre.append(gesture_handler)
            GestureOperator.isHandling = True
        # If we were handling scene changes, remove our handler from
        # the handler list by reverse enumerating and popping it off
        else:
            stop_operator()
        # Blender Python internals, must return {'FINISHED'}
        return {'FINISHED'}


def determine_current_gesture(current_frame):
    """Determine if within a gesture range

    Check to see if the current_frame is within any of the gestures'
    ranges, and set the current_gesture if so

    """
    # Reset current_gesture to -1, will remain so if current_frame is
    # not within a gesture
    # current_gesture = -1

    for i in range(GestureOperator.numGestures):
        # Note, gestureFrames[i][0] is the startingFrame of gesture i
        # and gestureFrames[i][1] is the endingFrame of gesture i
        if (current_frame >= GestureOperator.gestureFrames[i][0]
           and current_frame <= GestureOperator.gestureFrames[i][1]):
            GestureOperator.current_gesture = i
            break


# Stops the function of the addon by removing the scene handler we
# added to capture and send object positions, and TODO by closing the
# socket.
def stop_operator():
    # this prints out the full animation csv
    # print(GestureOperator.csvOutput)

    myHandlerList = bpy.app.handlers.scene_update_pre
    numHandlers = len(myHandlerList)
    for handlerID, function in enumerate(reversed(myHandlerList)):
        if function.__name__ == 'gesture_handler':
            myHandlerList.pop(numHandlers - 1 - handlerID)
    GestureOperator.isHandling = False

    # Tell the addon to reload the configs when it next executes
    GestureOperator.loadConfigs = True

    # Write out the CSV animation output to a file
    if GestureOperator.shouldOutputCSV:
        output_filepath = os.path.join(os.path.dirname(bpy.data.filepath),
                                       GestureOperator.csvOutputName)
        output_file = open(output_filepath, "w", encoding='utf-8')

        for gesture in range(GestureOperator.numGestures):
            # Get scene information for the current gesture
            gesture_start = GestureOperator.gestureFrames[gesture][0]
            gesture_end = GestureOperator.gestureFrames[gesture][1]

            # Translate each gesture so it starts at 0
            offset_index = 0

            # Range is not inclusive, so we loop over the start to end+1
            for scene_index in range(gesture_start, (gesture_end + 1)):
                scene = GestureOperator.csvOutput[scene_index]
                line = ""
                line += str(offset_index) + ", "

                # Write out the position of each object into columns of the CSV
                for i in range(GestureOperator.numObjects):
                    line += str(scene[i])
                    if i < (GestureOperator.numObjects - 1):
                        line += ", "

                line += "\n"
                output_file.write(line)

                offset_index += 1

            # Delimit each gesture with the proper character
            line = GestureOperator.gestureDelimiter
            line += "\n"
            output_file.write(line)

        output_file.close()
        print("File Closed")

    # Reset the CSV dictionary
    GestureOperator.csvOutput = {}


def register():
    """Registers the GestureOperator class with Blender.

    This is a required function for a Blender Add-On

    """
    bpy.utils.register_class(GestureOperator)


def unregister():
    """Unregisters the GestureOperator class with Blender.

    """
    bpy.utils.unregister_class(GestureOperator)


# For testing purposes, so the script will register the class when
# called directly
if __name__ == "__main__":
    register()
