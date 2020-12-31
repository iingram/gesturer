import struct
import socket
import curses
import time
import argparse
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument('-n',
                    '--num_servos',
                    required=True,
                    help='Number of servos to run.')
parser.add_argument('-i',
                    '--ip',
                    required=True,
                    help='IP of server host.')
parser.add_argument('-p',
                    '--port',
                    required=True,
                    help='Port number to use on server.')

args = parser.parse_args()
NUM_SERVOS = int(args.num_servos)
SERVER_IP = args.ip
PORT = int(args.port)  # often using 65432

servo_angles = [0] * NUM_SERVOS

current_servo_index = 0

status = ['Status string']


class SocketHandler(Thread):

    def __init__(self, num_servos, servo_angles, error):
        super().__init__()

        self.servo_angles = servo_angles

        self.sig = 'I' * num_servos

        sock = socket.socket()
        status[0] = 'Trying to connect to server'
        sock.connect((SERVER_IP, PORT))
        self.stream = sock.makefile('rwb')
        status[0] = 'Connected to server'

    def run(self):
        try:
            # read current servo angles over socket
            amount_to_read = struct.calcsize(self.sig)
            data = self.stream.read(amount_to_read)
            contents = struct.unpack(self.sig, data)
            for i, content in enumerate(contents):
                self.servo_angles[i] = contents[i]

            while True:
                to_send = struct.pack(self.sig, *self.servo_angles)
                # self.stream.write(struct.pack('<L', letter))
                self.stream.write(to_send)
                self.stream.flush()
                time.sleep(0.03)
        except Exception as e:
            print(type(e))
            print(e)
            self.stream.close()


def ui(stdscr):
    global current_servo_index
    global servo_angles
    global status

    key = None
    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while key != ord('q'):

        if key == curses.KEY_UP:
            current_servo_index += 1
            if current_servo_index > NUM_SERVOS - 1:
                current_servo_index = 0
        if key == curses.KEY_DOWN:
            current_servo_index -= 1
            if current_servo_index < 0:
                current_servo_index = NUM_SERVOS - 1
        if key == curses.KEY_RIGHT:
            servo_angles[current_servo_index] += 1
            if servo_angles[current_servo_index] > 180:
                servo_angles[current_servo_index] = 180
        if key == curses.KEY_LEFT:
            servo_angles[current_servo_index] -= 1
            if servo_angles[current_servo_index] < 0:
                servo_angles[current_servo_index] = 0

        stdscr.clear()

        strg = "Press 'q' to quit."
        stdscr.addstr(0, 0, strg, curses.color_pair(1))

        strg = 'Current Servo: {} which is at {} degrees.'
        strg = strg.format(current_servo_index,
                           servo_angles[current_servo_index])
        stdscr.addstr(1, 0, strg, curses.color_pair(3))

        strg = 'STATUS: ' + status[0]
        stdscr.addstr(2, 0, strg, curses.color_pair(3))

        curses.curs_set(0)
        stdscr.refresh()

        key = stdscr.getch()
        time.sleep(.01)


def main():
    socket_handler = SocketHandler(NUM_SERVOS,
                                   servo_angles,
                                   status)
    socket_handler.setDaemon(True)
    socket_handler.start()

    # sleep just a tiny bit so angles have been read from robot socket
    time.sleep(.01)
    curses.wrapper(ui)


if __name__ == '__main__':
    main()
