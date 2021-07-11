pythonGesturer
=====================

This program is used for communicating gestural information to an Arduino from properly formatted CSV files as well as a YAML configuration file. When used in conjuncture with the blenderGestuerAddon, this allows one to prototype gestures using Blender and then export them to a standalone CSV file, which can be played back on the robot using a computer running Python connected to an Arduino.

YAML is used to specify the number of servos in use and the number of gestures to be animated on the robot. The configs also specify the method of serial communication (identifying servo to write to based on an index value, or by the order in which values are received).


Dependencies
=====================

The non-standard dependencies to this addon are as follows: 

- serial 
- yaml


Usage
=====================

0. Copy the CSV output and the YAML configuration file from the Blender project in use (CSV output generated with the `blenderGestureAddon`) to the same directory as `pythonGesturer.py`.
1. Connect your Arduino to the computer, and change the serial port in the YAML configs to match that used by the Arduino.
2. Run the appropriate Ardunio recieveing code on the Arduino (generated with the instructions in `blenderGestureAddon`).
3. Run via the command line with `python pythonGesturer.py` and your animated gestures should play back on the connected robot. 
