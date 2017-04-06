
from aplayer import Aplayer
from input import Keypad
from time import sleep
import os


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
                self.song.append([0,2,4,7,9][index % 5]+12*(index//5)-12)
    def play(self,sp,mp):
        sp.play(0,0)
        sleep(6)
        sp.stop(0)
        for s in self.song:
            mp.play(0,s)
            sleep(1)
            mp.stop(0)






def main():
    player_start = Aplayer("deepfry", 1)
    player_main = Aplayer("deepfry2",1)
    s = SongBuilder(Keypad())
    while True:
        s.build()
        s.play(player_start,player_main)

if __name__=="__main__":
    main()