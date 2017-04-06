import time
import sys
import threading
from evdev import InputDevice, list_devices, ecodes


def seach_device(idstr):
    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
        print("found:", dev.name)
        if idstr in dev.name:
            return dev

    print('Joystick not found. Aborting ...')
    raise AssertionError("Device not found")


def seach_joystick():
    return seach_device("Dual Action")


def seach_keypad():
    return seach_device("Keypad")

def test_device(dev):
    print(" type| code|   value")
    for event in dev.read_loop():
        print("{:>5}|{:>5}|{:>10}".format(event.type,event.code,event.value))


class Keypad:
    def __init__(self):
        print("Setting up Keypad")
        self.device = seach_keypad()
    def key_gen(self):
        for event in self.device.read_loop():
            if event.type != 1:
                #check if event is a key related event
                continue
            elif event.value != 1:
                #check if ky is pressed (as opposed to released)
                continue
            elif event.code == 69:
                #check if key is nit general
                continue
            yield event.code


class Joystick:
    def __init__(self, index=0):
        print("Setting up Joystick")
        self.device = seach_joystick()
        self.axisvalues = [0, 0, 0, 0, 0, 0]
        self.keys = [0] * 12

        # self.proc = threading.Thread(None, self.process)
        # self.proc.start()

    def process(self):
        for event in self.device.read_loop():
            if event.type == 1 and 288 <= event.code < 300:
                self.keys[event.code - 288] = event.value
                yield "{}{}".format("ud"[event.value], event.code - 287)
            elif event.type == 3:
                axisindex = [0, 1, 2, 5, 16, 17].index(event.code)
                if event.code >= 16:
                    self.axisvalues[axisindex] = event.value
                else:
                    self.axisvalues[axisindex] = -(event.value < 63) + (event.value > 192)

    def test_key(self, index):
        return self.keys[index - 1]

    def axis(self, index):
        return self.axisvalues[index]

    def get_axis_pole(self, index):
        x = self.axisvalues[index * 2]
        y = self.axisvalues[index * 2 + 1]

        return ((0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)).index((x, y)) - 1


if __name__ == "__main__":

    if sys.argv[1] == "test":
        for c in Keypad().key_gen():
            print(c)
    #s = Joystick()
    #while True:
    #    s.process()
