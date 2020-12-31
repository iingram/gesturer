import struct
import socket
import time
import argparse
from threading import Thread

import yaml

from servo import Servo, prep_servo_board

parser = argparse.ArgumentParser()
parser.add_argument('config_file',
                    help='Gesturer Configuration File.')
args = parser.parse_args()
with open(args.config_file) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)

NUM_SERVOS = configs['numObjects']
IP = '0.0.0.0'
PORT = configs['robot_port']

servo_angles = [0] * NUM_SERVOS
SERVO_MIN = 0
SERVO_MAX = 180

current_servo_index = 0


class SocketHandler(Thread):

    def __init__(self, num_servos, servo_angles):
        super().__init__()

        self.sig = 'I' * num_servos
        self.servo_angles = servo_angles

        self.sock = socket.socket()
        self.sock.bind((IP, PORT))
        self.sock.listen()

    def run(self):
        while True:
            print('[INFO] Waiting for connection.')
            connection, address = self.sock.accept()
            print('[INFO] Connection made.')
            stream = connection.makefile('wrb')

            # send current servo angles over socket
            to_send = struct.pack(self.sig, *servo_angles)
            stream.write(to_send)
            stream.flush()

            while True:
                amount_to_read = struct.calcsize(self.sig)
                data = stream.read(amount_to_read)
                if not data:
                    break

                contents = struct.unpack(self.sig, data)
                for i, content in enumerate(contents):
                    self.servo_angles[i] = contents[i]

            print('[INFO] Socket disconnected.')
            stream.close()


class ServoController(Thread):

    def __init__(self, num_servos, servo_angles):
        super().__init__()

        self.servo_angles = servo_angles

        bus = prep_servo_board()

        self.servos = []
        for i in range(num_servos):
            self.servos.append(Servo(bus, i))

    def run(self):
        while True:
            print(servo_angles)
            for index, servo in enumerate(self.servos):
                command = self.servo_angles[index]
                if command < SERVO_MIN:
                    command = 0
                elif command > SERVO_MAX:
                    command = SERVO_MAX
                servo.command_angle(command)
            time.sleep(0.03)


def main():
    comms = SocketHandler(NUM_SERVOS, servo_angles)
    comms.start()

    servo_controller = ServoController(NUM_SERVOS, servo_angles)
    servo_controller.setDaemon(True)
    servo_controller.start()


if __name__ == '__main__':
    main()
