
from aplayer import Aplayer
from input import Keypad
from time import time,sleep
import subprocess as sp
import os, shutil
from random import randrange

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
    def concat(self):
        os.unlink('sounds/result.wav')
        print("building full song")
        sp.Popen(("sox","sounds/intro.wav")+ tuple("sounds/base{}_{}.wav".format(randrange(6),index) for index in self.song) + ('sounds/result.wav',),
                 shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE).wait()
        print("done building song")
    def play(self):
        sp.Popen(("aplay",'sounds/result.wav',),
                 shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)


def filebuilder():
    folder = 'sounds/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    print("buidling sound files")
    procs = []
    #create intro
    procs.append(sp.Popen(("sox","deepfry.wav","sounds/intro.wav","trim","0","6"),
             shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    #create sound
    for vars in range(6):
        procs.append(sp.Popen(("sox", "deepfry.wav", "sounds/base{}.wav".format(vars), "trim", str(4+vars), "1"),
                 shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))

    #create notes
    for vars in range(6):
        for c in range(20):
            pitch = [0,2,4,7,9][c % 5]+12*(c//5)-12
            procs.append(sp.Popen(("sox", "sounds/base.wav", "sounds/base{}_{}.wav".format(vars,c), "pitch", "{:+}".format(pitch*100)),
                     shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    print("waiting for processes")
    #print(procs)
    [p.wait() for p in procs]
    print("done building soundfiles")

def spinsleep(seconds):
    start = time()
    if seconds > 1:
        sleep(seconds - 1)
    while time() < start + seconds:
        pass



def main():
    say("starting music server")
    filebuilder()
    s = SongBuilder(Keypad())
    say("ready for some music")
    while True:
        s.build()
        s.concat()
        s.play()


if __name__=="__main__":
    main()