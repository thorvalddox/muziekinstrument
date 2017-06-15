

from input import Keypad
from time import time,sleep
import subprocess as sp
import os
from random import randrange

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
        try:
            os.remove('sounds/result.wav')
        except FileNotFoundError:
            pass
        print("building full song")
        sp.Popen(("sox","sounds/intro.wav")+ tuple("sounds/base{}_tune{}.wav".format(randrange(4,10),index) for index in self.song) + ('sounds/result.wav',),
                 shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE).wait()
        print("done building song")
    def play(self):
        sp.Popen(("aplay",'sounds/result.wav',),
                 shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)


class Filebuilder:
    def __init__(self):
        folder = 'sounds/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.procs = []
        self.variants = []
        self.create_intro()
        for i in range(4,10):
            self.create_base_sound(i)
        self.wait()
        self.repitch_sound([0,2,4,7,9][c % 5]+12*(c//5)-12 for c in range(20))
    def wait(self):
        [p.wait() for p in self.procs]
    def new_proc(self,*args):
        self.procs.append(sp.Popen(args,
                              shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    def create_intro(self):
        self.new_proc("sox", "deepfry.wav", "sounds/intro.wav", "trim", "0", "6")
    def create_base_sound(self,index):
        self.new_proc("sox", "deepfry.wav", "sounds/base{}.wav".format(index), "trim", "{}".format(index), "1")
        self.variants.append(index)
    def repitch_sound(self,pitches):
        for index in self.variants:
            for i,pitch in enumerate(pitches):
                self.new_proc("sox", "sounds/base{}.wav".format(index), "sounds/base{}_tune{}.wav".format(index,i),
                              "pitch", "{:+}".format(pitch * 100))




def filebuilder():
    folder = 'sounds/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("buidling sound files")
    procs = []
    #create intro
    procs.append(sp.Popen(("sox","deepfry.wav","sounds/intro.wav","trim","0","6"),
             shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))
    #create sound
    procs.append(sp.Popen(("sox", "deepfry.wav", "sounds/base.wav", "trim", "6", "1"),
             shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE))

    [p.wait() for p in procs]
    #create notes

    for c in range(20):
        pitch = [0,2,4,7,9][c % 5]+12*(c//5)-12
        procs.append(sp.Popen(("sox", "sounds/base.wav", "sounds/base{}.wav".format(c), "pitch", "{:+}".format(pitch*100)),
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
    #filebuilder()
    Filebuilder()
    s = SongBuilder(Keypad())
    say("ready for some music")
    while True:
        s.build()
        s.concat()
        s.play()


if __name__=="__main__":
    main()