blenderGestureAddon
=====================

Addon for real-time robotic gesture development with [Blender](https://www.blender.org/) and Arduino based robots. 

This extension to Blender allows the user to generate and play back animations generated in Blender on robots, in real time.

YAML is used to specify the configurations of the Blender objects and the associated robotic components, and these configurations are read in by the Blender addon. These configurations are also used by a Python script to generate the Arduino code necessary for the desired robot to communicate with the addon properly.


Dependencies
=====================
Note: Dependencies can now be installed via the `deploy.sh` script!

To run this plugin, you must install some additional Python libraries inside of Blender, as Blender comes packaged with its own version of Python (in case the user does not have it). So you must install the following libraries to `/blender/2.xy/python/lib/python3.4/` (for MacOS, `/blender.app/Contents/Resources/2.xy/python/lib/python3.4/`):

- [pyserial](https://github.com/pyserial/pyserial) 
- [pyyaml](http://pyyaml.org/wiki/PyYAML) (note, with `pyyaml` copy the `lib3/yaml` folder, not the `lib/yaml` folder).



Setup
=====================

0. Run `deploy.sh`.
1. Follow the given prompts to work with a fresh Blender install, or to specify the paths for the local copy's internal Python library and addons directory.
2. You now have the required dependencies and the `gestureDeveloper.py` addon installed in the desired copy of Blender!

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
5. Navigate to `File/User Preferences/Add-ons`.
6. Select the "Object" category.
7. Find "Object: Gesture Operator" addon and select the checkbox next to it.
8. If you wish for the addon to be loaded every time you start up Blender (useful for development), click the `Save User Settings` button in the lower left corner.
9. To activate the addon, press the spacebar while in Blender to bring up the search interface, type "Gesture Operator", and select the result.
10. To deactivate the addon once it is running, follow the same process as in step 6.
