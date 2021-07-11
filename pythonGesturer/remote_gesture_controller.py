"""Controls gestures on a hobby-servo-actuated robot over TCP/IP
socket, playing gestures back from csv files produced from Blender
gesturer tools.

"""
import argparse
import csv
import socket
import struct

import time
from threading import Thread

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('config_file',
                    help='YAML file containing configuration info.')
parser.add_argument('-i',
                    '--ip',
                    required=True,
                    help='IP of server host.')
parser.add_argument('-p',
                    '--port',
                    required=True,
                    help='Port number to use on server.')

args = parser.parse_args()
SERVER_IP = args.ip
PORT = int(args.port)  # often using 65432

filename = args.config_file
with open(filename) as f:
    stream = f.read()
    configs = yaml.load(stream, Loader=yaml.Loader)

NUM_SERVOS = configs["numObjects"]
NUM_GESTURES = configs["numGestures"]
CSV_ANIMATION_FILENAME = configs["csvOutputName"]

servo_angles = [0] * NUM_SERVOS

# Value to represent the new gesture to be performed, when this value is
# changed in update_gesture() the program smooths between the current gesture
# and this new gesture


def update_gesture(current_frame, current_gesture, num_frames_in_gesture):
    if current_frame >= num_frames_in_gesture - 1:
        new_gesture = current_gesture + 1
        if new_gesture >= NUM_GESTURES:
            new_gesture = 0
    else:
        new_gesture = current_gesture

    return new_gesture


class ServoCommandHandler(Thread):

    def __init__(self, NUM_SERVOS, servo_angles):
        super().__init__()

        self.servo_angles = servo_angles

        self.sig = 'I' * NUM_SERVOS

        sock = socket.socket()
        sock.connect((SERVER_IP, PORT))
        self.stream = sock.makefile('wb')

    def run(self):
        try:
            while True:
                to_send = struct.pack(self.sig, *servo_angles)
                self.stream.write(to_send)
                self.stream.flush()
                time.sleep(0.03)
        except Exception as e:
            print(type(e))
            print(e)
            self.stream.close()


def frame_handler(current_frame, gesture_positions):
    global servo_angles
    for i in range(len(servo_angles)):
        # We index plus 1 into the gesture_positions since the first
        # column is the frame index
        servo_angle = int(gesture_positions[current_frame][i + 1])
        # servo_angle -= 120
        if (servo_angle > 180):
            servo_angle = 180
        elif (servo_angle < 0):
            servo_angle = 0
        servo_angles[i] = servo_angle
        # print("Servo " + str(i) + " is: " + str(servo_angle))


def main():

    servo_command_handler = ServoCommandHandler(NUM_SERVOS, servo_angles)
    servo_command_handler.start()

    # read in animation information from csv file
    with open(CSV_ANIMATION_FILENAME, 'rt') as f:
        reader = csv.reader(f)
        # A list of gesture animations, each containing a list of the
        # positions for each motor at each frame of the gesture
        csv_gesture_data = []
        for gesture in range(NUM_GESTURES):
            # Append a list for each gesture
            csv_gesture_data.append([])
        csv_gesture_length = [0] * NUM_GESTURES

        gestureCount = 0
        # Read through the CSV file and populate the gesture data/length arrays
        for row in reader:
            # If the first item in the CSV row is a "*", we have
            # reached the end of a gesture
            if row[0] == "*":
                length = len(csv_gesture_data[gestureCount])
                csv_gesture_length[gestureCount] = length
                gestureCount += 1
            # Otherwise, continue adding to the current gesture
            else:
                csv_gesture_data[gestureCount].append(row)

        # In case there was no "*" at the end of the last gesture, we
        # set the last gesture length
        if gestureCount == (NUM_GESTURES - 1):
            length = len(csv_gesture_data[gestureCount])
            csv_gesture_length[gestureCount] = length

    # # Set frame rate and corresponding sleep rate
    # frameRate = 24
    # sleepTime = 1./frameRate
    # start_time = time.time()

    current_gesture = 0
    # Start the number of frames as the length of the current_gesture
    num_frames_in_gesture = csv_gesture_length[current_gesture]

    while True:
        for current_frame in range(num_frames_in_gesture):
            frame_handler(current_frame,
                          csv_gesture_data[current_gesture])

            print('{}: {}: {}'.format(current_gesture,
                                      current_frame,
                                      servo_angles))
            time.sleep(.03)

            # LOGIC FOR SWITCHING GESTURES GOES HERE
            new_gesture = update_gesture(current_frame,
                                         current_gesture,
                                         num_frames_in_gesture)

            # mechanics for switching gesture if necessary
            if current_gesture != new_gesture:
                print("Switching Gestures...")
                print("current_gesture is: " + str(current_gesture))
                print("new_gesture is: " + str(new_gesture))
                # startPosArray = [0] * NUM_SERVOS
                # endPosArray = [0] * NUM_SERVOS
                # oldGesture = current_gesture
                current_gesture = new_gesture
                # startPosArray = csv_gesture_data[oldGesture][current_frame]
                # endPosArray = csv_gesture_data[current_gesture][0]
                num_frames_in_gesture = csv_gesture_length[current_gesture]

                # BE SURE TO "break" AT THE END OF THE SWITCHING GESTURES LOGIC
                break

            # # If rendering the frame on the robot took less time than
            # # the sleep time, subtract the time_difference from the
            # # sleepTime and sleep that amount to create the proper
            # # frame rate
            # time_difference = time.time() - start_time
            # if time_difference < sleep_time:
            #     time.sleep(sleep_time - time_difference)
            # else:
            #     print("Program execution time exceeded the frame rate...")

            # Otherwise, we do not want to sleep as we have already spent more
            # time than the frame rate
            # start_time = time.time()


if __name__ == "__main__":
    main()
