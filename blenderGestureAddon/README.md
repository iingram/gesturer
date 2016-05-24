blenderGestureAddon
=====================

Addon for real-time robotic gesture development with [Blender](https://www.blender.org/) and Arduino based robots. 

This extension to Blender allows the user to create a mapping from the motion of Blender objects to the movement of hobby servos, allowing one to prototype robotic gestures on arbitrary architectures in real-time. 

YAML is used to specify the configurations of the Blender objects and the associated robotic components, and these configurations are read in by the Blender addon. These configurations are also used by a Python script to generate the Arduino code necessary for the desired robot to communicate with the addon properly.


Dependencies
=====================

This plugin comes packaged with the most recent (as of the latest commit) versions its dependencies .


Setup
=====================


0. Open Blender.
1. Open `File->User Preferences`.
2. Navigate to the `Add-ons` tab.
3. Click `Install from File...` and select `addon-gestureDeveloper.zip` to install the addon.
4. Check the box next to `Object: Gesture Operator` to enable.
    * To enable the addon across Blender restarts, click `Save User Settings`.


Usage
=====================

0. Configure `gesturerConfigs.yaml` to match your Blender and hardware setup (e.g. desired object names/axes, serial port to use, etc.)
1. Run `generateArduino.py` with `gesturerConfigs.yaml` and `motors_template.ino` present in the current directory to generate Arduino code.
3. Upload this generated code to your robot, and leave your robot connected to the computer.
4. Open the proper `.blend` file in Blender.
    * Provided Blender File: 
        - Open Blender (via the command line if you want to see Python output, which is recommended).
        - Navigate to `gesturer/blenderGestureAddon/` and open the file `prototype_gesture_addon_scene_handler.blend`.
    * General Blender File: 
        - Put `gesturerConfigs.yaml` in the same folder as the `.blend` file you are using.
        - Open Blender (if via the command line, watch the output as you go through the steps below to make sure you don't get any fatal errors!).
        - Navigate to and open your `.blend` file.
5. To activate the addon, press the spacebar while in Blender to bring up the search interface, type "Gesture Operator", and select the result.
6. To deactivate the addon once it is running, follow the same process from step 5. If set in the YAML configs, deactivating the addon will output a CSV file containing the animated gestures. Make sure to run through the entire window of each gesture in Blender or you will get an error.
