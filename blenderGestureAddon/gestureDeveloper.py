import bpy
import serial
import yaml
import os
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
serialPort = serial.Serial('/dev/tty.usbmodem1411', 9600)
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


    # Hardcode the object we want selected to be the body of the magpie 

    # Generalized loop for putting an arbitrary number of object parameters out 
    # on the serial connection
    for i in range(GestureOperator.numObjects):
        object = bpy.data.objects[GestureOperator.objectNames[i]]
        movement = degrees(object.rotation_euler[GestureOperator.objectAxes[i]])
        servoAngle = chr(int(GestureOperator.objectOffsets[i] + movement))
        print("Servo" + str(i) + " angle is: " + str(ord(servoAngle)))
        #serialPort.write(chr(i + 181).encode())
        serialPort.write(servoAngle.encode())
   

# GestureOperator class
class GestureOperator(bpy.types.Operator): 
    # Blender Addon internals 
    bl_idname = "object.gesture_operator"  
    bl_label = "Gesture Operator"  
    
    # Raw configuration data
    configs = {}
    # Extracted configuration data
    objectNames = []
    objectAxes = []
    objectOffsets = []
    numObjects = []

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
      

# Attempt to add a button for performing the "Gesture Operator"
def add_object_button(self, context):  
    self.layout.operator(  
        GestureOperator.bl_idname,  
        text=GestureOperator.__doc__,  
        icon='PLUGIN') 


# Register the GestureOperator class with Blender  
def register():  
    bpy.utils.register_class(GestureOperator) 
    # Add the button for activating the "Gesture Operator" to the 3d View
    # bpy.types.VIEW3D_MT_object.append(add_object_button) 

# For testing purposes, so the script will register the class when called directly
if __name__ == "__main__":  
    register()  