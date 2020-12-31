import time

import smbus


def prep_servo_board():
    bus = smbus.SMBus(1)
    addr = 0x40

    # enable word writes
    bus.write_byte_data(addr, 0, 0x20)
    time.sleep(.25)

    # enable Prescale change as noted in the datasheet
    bus.write_byte_data(addr, 0, 0x10)
    # delay for reset
    time.sleep(.25)

    # change the Prescale register value for 50 Hz, using the equation
    # in the datasheet.
    bus.write_byte_data(addr, 0xfe, 0x79)

    # enables word writes
    bus.write_byte_data(addr, 0, 0x20)
    time.sleep(.25)

    return bus


class Servo():

    def __init__(self, bus, channel=0):
        self.ZERO_POINT = 209  # 170
        self.bus = bus
        self.addr = 0x40
        start_address = 6 + 4*channel
        self.stop_address = start_address + 2

        # start time = 0us
        self.bus.write_word_data(self.addr, start_address, 0)

        # end time = 1.0ms (0 degrees)
        self.bus.write_word_data(self.addr, self.stop_address, self.ZERO_POINT)

    def command_angle(self, angle):
        end_time = int(self.ZERO_POINT + 205*(angle/90))
        self.bus.write_word_data(self.addr, self.stop_address, end_time)

    def turn_off(self):
        self.bus.write_word_data(self.addr, self.stop_address, 0)
