blenderGestureAddon
=====================

Addon for incorporating [gesturer](https://github.com/iingram/gesturer) with [Blender](https://www.blender.org/) 3d modeling. 

This extension to Blender allows the user to generate and play back animations generated in Blender on robots, in real time.

YAML will be used to specify the configurations of the Blender objects and the associated robotic components. 


Dependencies
=====================
To run this plugin, you must install some additional Python libraries inside of Blender, as Blender comes packaged with its own version of Python (in case the user does not have it). So you must install the following libraries to `/blender/2.xy/python/lib/python3.4/` (for MacOS, `/blender.app/Contents/Resources/2.xy/python/lib/python3.4/`):

- [pyserial](https://github.com/pyserial/pyserial) 
- [pyyaml](http://pyyaml.org/wiki/PyYAML) (note, with `pyyaml` copy the `lib3/yaml` folder, not the `lib/yaml` folder).



Setup
=====================

TODO: create a setup script that copies the addon into the proper directory
- Make sure you have a properly formatted `gesturerConfigs.yaml` in the same directory as the `.blend` file you are working with.

Running
=====================

0. Connect Arduino (running the receiving software) based robot to computer.
1. Open `prototype_gesture_addon_scene_handler.blend` with Blender (via the command line if you want to see Python output, which is recommended). 
2. Go to the "Scripting" view. 
3. Press the "Run Script" button.
4. Animate with the robot.
