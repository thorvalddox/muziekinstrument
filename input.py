import time
import sys
import threading
from evdev import InputDevice, list_devices, ecodes


def seach_joystick():
    found = False
    devices = [InputDevice(fn) for fn in list_devices()]
    for dev in devices:
        print(dev.name)
        if "Joystick" in dev.name or "Dual" in dev.name:
            found = True
            return dev

    if not found:
        print('Joystick not found. Aborting ...')
        sys.exit()



class Joystick:
    def __init__(self,index=0):
        print("Setting up Joystick")
        self.device = seach_joystick()
        self.axisvalues = [0,0,0,0,0,0]
        self.keys = [0]*12

        #self.proc = threading.Thread(None, self.process)
        #self.proc.start()


    def process(self):
        for event in self.device.read_loop():
            if event.type == 1 and 288 <= event.code < 300:
                self.keys[event.code-288] = event.value
                yield "{}{}".format("ud"[event.value],event.code-287)
            elif event.type == 3:
                axisindex = [0,1,2,5,16,17].index(event.code)
                if event.code >= 16:
                    self.axisvalues[axisindex] = event.value
                else:
                    self.axisvalues[axisindex] = -(event.value<63) + (event.value>192)

    def test_key(self,index):
        return self.keys[index-1]

    def axis(self,index):
        return self.axisvalues[index]


    def get_axis_pole(self,index):
        x = self.axisvalues[index*2]
        y = self.axisvalues[index*2+1]

        return ((0,0),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,1)).index((x,y)) - 1



if __name__ == "__main__":
    s = Joystick()
    while True:
        s.process()

