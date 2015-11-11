blenderGestureAddon
=====================

Addon for incorporating [gesturer](https://github.com/iingram/gesturer) with [Blender](https://www.blender.org/) 3d modeling. 

This extension to Blender allows the user to generate and play back animations generated in Blender on robots, in real time.

YAML will be used to specify the configurations of the Blender objects and the associated robotic components. 


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

0. Connect Arduino (running the receiving software) based robot to computer.
1a. Standard Usage: Open `prototype_gesture_addon_scene_handler.blend` with Blender (via the command line if you want to see Python output, which is recommended).
1b. More general usage: 
    -Modify gesturerConfigs.yaml to match the parameters you desire to use from your `.blend` file and for your hardware setup (object names, desired axes, serial port, etc.).
    -Put `gesturerConfigs.yaml` in the same folder as the `.blend` file you are using.
    -Open Blender via the command line (watch the command line as you go through the steps below to make sure you don't get any fatal errors!).
    -Navigate to and open your `.blend` file.
2. Navigate to `File/User Preferences/Add-ons`.
3. Select the "Object" category.
4. Find "Object: Gesture Operator" addon and select the checkbox next to it.
5. If you wish for the addon to be loaded every time you start up Blender (useful for development), click the `Save User Settings` button in the lower left corner.
6. To activate the addon, press the spacebar while in Blender to bring up the search interface, type "Gesture Operator", and select the result.
7. To deactivate the addon once it is running, follow the same process as in step 6.
