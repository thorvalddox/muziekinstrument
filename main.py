from input import Joystick
from output import Soundhandler
from collections import namedtuple
from math import floor
from time import sleep,time
import json
from waveplayer import WavePlayer

Tune = namedtuple("Tune","letter,octave,change")


def get_tune_idc(tune):
    return \
        {"a": 0, "b": 2, "c": -9, "d": -7, "e": -5, "f": -4, "g": -2}[tune.letter] + \
        tune.octave * 12 + \
        tune.change

def get_frequency(tune):

    return floor(440 * 2**(get_tune_idc(tune)/12))

def get_tune(diff):
    for t in all_tunes(-3,+3):
        if get_tune_idc(t) == diff:
            return t

def build_mayor(ground):
    idc = get_tune_idc(ground)
    yield ground
    yield get_tune(idc+4)
    yield get_tune(idc+7)

def build_minor(ground):
    idc = get_tune_idc(ground)
    yield ground
    yield get_tune(idc + 3)
    yield get_tune(idc + 7)

def all_tunes(low,high):
    for o in range(low,high+1):
        for t in "acdefg":
            for c in [-1,0,1]:
                yield Tune(t,o,c)

def forceplay_tune(sh,tune,time):
    play_chord(sh,[tune])
    spinsleep(time*(0.5))
    stop_chord(sh,[tune])

def play_chord(sh,tunes):
    ground = tunes[0]
    for tune in tunes:
        sh.play(ground,get_frequency(tune))


def stop_chord(sh, tunes):
    ground = tunes[0]
    for tune in tunes:
        sh.stop(ground, get_frequency(tune))

def spinsleep(seconds):
    start = time()
    if seconds > 1:
        sleep(seconds - 1)
    while time() < start + seconds:
        pass


def auto_tune_player(sh,string):
    if string.startswith("$"):
        w = WavePlayer(string[1:])
        w.play()
        w.wait()
        return
    speed,keys = string.split(":")
    timeset = 60/int(speed)*4
    octave = 0
    octavechange = 0
    change = 0
    speed = 4
    breaknote = 1
    for l in string:
        if l in "abcdefg":
            if breaknote:
                spinsleep(0.1)
            forceplay_tune(sh,Tune(l,octave+octavechange,change),speed*timeset-0.1*breaknote)

            #print(Tune(l, octave + octavechange, change))
            change = 0
            octavechange = 0
            breaknote = 1

        elif l in "x#$%":
            change = 2-"x# $%".index(l)
        elif l in "+-":
            octave += 1 if l=="+" else -1
        elif l in "^v":
            octavechange += 1 if l == "^" else -1
        elif l in "1248":
            speed = 1/int(l)
        elif l in "o'*":
            speed = 1 / {"o":16,"'":32,"*":64}
        elif l in "/":
            spinsleep(speed*timeset)
        elif l in "_":
            breaknote = 0









def main():
    j = Joystick()
    sh = Soundhandler()
    with open("tunes.json") as file:
        songs = json.load(file)
    print("READY")
    while True:

        if j.get_free("b12"):
            z = j.get_axis_pole("r")
            if z >= 0:
                try:
                    s = songs[z]
                except IndexError:
                    s = "100:4+cccccccc"
                auto_tune_player(sh, s)



        for t in all_tunes(-1,2):
            if t.octave != j.get_free("b5") - j.get_free("b7"):
                stop_chord(sh,[t])
            elif not j.get_free({"c":"b1","d":"b2","e":"b3","f":"b4","g":"b6","a":"b8"}[t.letter]):
                stop_chord(sh, [t])
            elif t.change != j.get_hat(0,True) - j.get_hat(0,False):
                stop_chord(sh, [t])
            else:
                if j.get_hat(1,True):
                    play_chord(sh,list(build_mayor(t)))
                elif j.get_hat(1,False):
                    play_chord(sh, list(build_minor(t)))
                else:
                    play_chord(sh, [t])






if __name__ == "__main__":
    main()






