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
        self.codes = {}
        #self.proc = threading.Thread(None, self.process)
        #self.proc.start()


    def process(self):
        pass
        #for event in self.device.read_loop():
            #self.codes[(event.code,event.type)] = event.value


    def get_code(self,code,type_):
        print()
        return self.codes.get((code,type_),0)


    def get_hat(self,index,up):
        return self.get_code(16+index, 3) == [-1,1][up]

    def get_axis(self,index,up):
        axis = [0,1,2,5][index]
        return (self.get_code(axis,3)-127)/255* [-1,1][up] > 0.7


    def get_key(self, index):
        return 287 + index in self.device.active_keys()

    def get_free(self,idstring):
        if idstring[0] == "b":
            return self.get_key(int(idstring[1:]))
        elif idstring[0] == "l":
            return self.get_axis(0,idstring[1] in "+dl") and self.get_axis(1,idstring[1] in "+dl")
        elif idstring[0] == "r":
            return self.get_axis(2, idstring[1] in "+dl") and self.get_axis(3, idstring[1] in "+dl")
        elif idstring[0] == "h":
            return self.get_hat(0, idstring[1] in "+dl") and self.get_axis(1, idstring[1] in "+dl")


    def get_axis_pole(self,axis):
        if axis == "l":
            x = self.get_axis(0,True) - self.get_axis(0,False)
            y = self.get_axis( 1, True) - self.get_axis( 1, False)
        if axis == "r":
            x = self.get_axis(2, True) - self.get_axis(2, False)
            y = self.get_axis(3, True) - self.get_axis(3, False)
        if axis == "h":
            x = self.get_hat(0, True) - self.get_hat(0, False)
            y = self.get_hat(1, True) - self.get_hat(1, False)
        return ((0,0),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,1)).index((x,y)) - 1



if __name__ == "__main__":
    s = Joystick()
    while True:
        s.process()

