
from aplayer import Aplayer
from input import Keypad
from time import time,sleep
import subprocess as sp
import os
import json


def say(text):
    os.system("espeak \"{}\"".format(text))



class SongBuilder():
    def __init__(self,keypad):
        self.song = []
        self.keypad = keypad
        self.keygen = self.keypad.key_gen
    def build(self):
        self.song = []
        for key in self.keygen():
            if key == "n":
                return
            if key == "<" and self.song:
                self.song.pop()
            if key in "0123456789":
                index = "0123456789".index(key)
                self.song.append(index)
    def play(self,sp,mp,influence=1):
        sp.play(0,0)
        spinsleep(6)
        sp.stop(0)
        mp.play(0,0)
        channel = False
        # for s in self.song:
        #     mp.play(channel,s)
        #     spinsleep(influence)
        #     sp.stop(0)
        #     mp.stop(not channel)
        #     channel ^= True
        #     spinsleep(1-influence)
        for s in self.song:
            mp.play(0,s)
            spinsleep(5)
        spinsleep(6)
        mp.stop(0)
        mp.stop(1)
        sp.stop(0)


def filebuilder():
    print("buidling sound files")
    procs = []
    #create intro
    procs.append(sp.Popen(("sox","deepfry.wav","sounds/intro.wav","trim","0","6"),
             shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    #create sound
    procs.append(sp.Popen(("sox", "deepfry.wav", "sounds/base.wav", "trim", "6", "7"),
             shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    #create notes
    for c in range(20):
        pitch = [0,2,4,7,9][c % 5]+12*(c//5)-12
        procs.append(sp.Popen(("sox", "sounds/base.wav", "sounds/base{}.wav".format(c), "pitch", "{:+}".format(pitch*100)),
                 shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    print("waiting for processes")
    [p.wait for p in procs()]
    print("done building soundfiles")

def spinsleep(seconds):
    start = time()
    if seconds > 1:
        sleep(seconds - 1)
    while time() < start + seconds:
        pass



def main():
    filebuilder()
    s = SongBuilder(Keypad())
    while True:
        s.build()


if __name__=="__main__":
    main()