import struct
import socket
import time
import argparse
from threading import Thread

from servo import Servo, prep_servo_board

parser = argparse.ArgumentParser()

parser.add_argument('-n',
                    '--num_servos',
                    required=True,
                    help='Number of servos to run.')
parser.add_argument('-i',
                    '--ip',
                    required=True,
                    help='IP of host server.')
parser.add_argument('-p',
                    '--port',
                    required=True,
                    help='Port number to use on server. Often using 65432')

args = parser.parse_args()
NUM_SERVOS = int(args.num_servos)
IP = args.ip
PORT = int(args.port)  # often using 65432

servo_angles = [0] * NUM_SERVOS

current_servo_index = 0

SERVO_MIN = 0
SERVO_MAX = 180


class SocketHandler(Thread):

    def __init__(self, num_servos, servo_angles):
        super().__init__()

        self.sig = 'I' * num_servos
        self.servo_angles = servo_angles

        sock = socket.socket()
        sock.bind((IP, PORT))
        sock.listen()
        print('[INFO] Waiting for connection.')
        connection, address = sock.accept()
        print('[INFO] Connection made.')

        self.stream = connection.makefile('rb')

    def run(self):
        try:
            while True:
                amount_to_read = struct.calcsize(self.sig)
                data = self.stream.read(amount_to_read)
                contents = struct.unpack(self.sig, data)
                for i, content in enumerate(contents):
                    self.servo_angles[i] = contents[i]

                # if letter == ord('q'):
                #     break
        except KeyboardInterrupt as e:
            print(e)
            print('Received keyboard interrupt')
        except Exception as e:
            print(type(e))
            print('Socket connection failed.'
                  + ' Maybe socket closed/ended on client side?')
        finally:
            print('Closing up shop.')
            self.stream.close()
            # self.connection.close()
            # self.sock.close()


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
    servo_controller.start()


if __name__ == '__main__':
    main()
