from input import Joystick
from aplayer import Aplayer
from collections import namedtuple
from math import floor
from time import sleep, time
import json
import os

Tune = namedtuple("Tune", "letter,octave,change")


def get_tune_idc(tune):
    return \
        {"a": 0, "b": 2, "c": -9, "d": -7, "e": -5, "f": -4, "g": -2}[tune.letter] + \
        tune.octave * 12 + \
        tune.change


def get_frequency(tune):
    return floor(440 * 2 ** (get_tune_idc(tune) / 12))


def get_tune(diff):
    for t in all_tunes(-3, +3):
        if get_tune_idc(t) == diff:
            return t


def build_mayor(ground):
    idc = get_tune_idc(ground)
    yield ground
    yield get_tune(idc + 4)
    yield get_tune(idc + 7)


def build_minor(ground):
    idc = get_tune_idc(ground)
    yield ground
    yield get_tune(idc + 3)
    yield get_tune(idc + 7)


def all_tunes(low, high):
    for o in range(low, high + 1):
        for t in "acdefg":
            for c in [-1, 0, 1]:
                yield Tune(t, o, c)


def forceplay_tune(sh, tune, seconds):
    play_chord(sh, 0, [tune])
    sleep(seconds)
    stop_chord(sh, 0)


def stick_keyid(defid, tunes):
    keys = [defid, 12, 13]
    for i, t in enumerate(tunes):
        yield keys[i], t


def make_chord(sh, keyid, ground, tunetype):
    if tunetype == 1:
        tunes = build_mayor(ground)
    elif tunetype == -1:
        tunes = build_minor(ground)
    else:
        tunes = [ground]
    play_chord(sh, keyid, tunes)


def play_chord(sh, keyid, tunes):
    for key, tune in stick_keyid(keyid, tunes):
        sh.play(key, get_tune_idc(tune))


def stop_chord(sh, keyid):
    sh.stop(keyid)
    sh.stop(12)
    sh.stop(13)
    sh.stop(0)


def spinsleep(seconds):
    start = time()
    if seconds > 1:
        sleep(seconds - 1)
    while time() < start + seconds:
        pass


def auto_tune_player(sh, string):
    if string.startswith("$"):
        sh.play_media(string[1:])
        return
    speed, keys = string.split(":")
    timeset = 60 / int(speed) * 2
    octave = 0
    octavechange = 0
    change = 0
    speed = 4
    breaknote = 1
    for l in string:
        if l in "abcdefg":
            if breaknote:
                spinsleep(0.1)
            forceplay_tune(sh, Tune(l, octave + octavechange, change), speed * timeset - 0.1 * breaknote)

            # print(Tune(l, octave + octavechange, change))
            change = 0
            octavechange = 0
            breaknote = 1

        elif l in "x#$%":
            change = 2 - "x# $%".index(l)
        elif l in "+-":
            octave += 1 if l == "+" else -1
        elif l in "^v":
            octavechange += 1 if l == "^" else -1
        elif l in "1248":
            speed = 1 / int(l)
        elif l in "o'*":
            speed = 1 / {"o": 16, "'": 32, "*": 64}[l]
        elif l in "/":
            sleep(speed * timeset)
        elif l in "_":
            breaknote = 0


def say(text):
    os.system("espeak \"{}\"".format(text))


def change_tune(tune,ocswap,cswap):
    return Tune(tune.letter,tune.octave + ocswap,tune.change + cswap)

class Scale:
    def __init__(self,ground_letter,kind="may"):
        ground = Tune(ground_letter,-(ground_letter in "ab"),0)
        if kind=="may":
            add = [0,2,4,5,7,9]
        elif kind=="min":
            add = [0,2,3,5,7,10]
        elif kind=="penta":
            add = [0,2,4,7,9]
        elif kind=="quat":
            add = [0,3,6,9]
        else:
            add = 0
        self.modes = [None,None]
        self.tones = [change_tune(ground,0,x) for x in add]
        if len(add) == 4:
            self.mode[0] = ModeHandler({1:0,2:1,3:2,4:3},{5:+1,7:-1,6:+3,8:-3})
            self.mode[1] = ModeHandler({1:0,2:1,3:2,4:3},{5:+1,7:-1,6:+3,8:-3})
        if len(add) == 5:
            self.mode[0] = ModeHandler({1:0,2:1,3:2,4:3,6:4},{5:+1,7:-1})
            self.mode[1] = ModeHandler({1:1,2:2,4:4,6:0,8:3},{5:+1,7:-1})
        if len(add) == 6:
            self.mode[0] = ModeHandler({1:0,2:1,3:2,4:3,6:4,8:5},{5:+1,7:-1})
            self.mode[1] = ModeHandler({1:1,2:2,3:3,4:5,6:0,8:4},{5:+1,7:-1})

    def play_note(self,sh,j,key,mode):
        self.modes[mode].play_note(sh,j,key,self.tones)



class ModeHandler:
    def __init__(self,notebuttons,octavedict):
        self.notebuttons = notebuttons #dict button:index
        self.octavedict = octavedict #dict button:shift
    def play_note(self,sh,j,key,tones):
        keyindex = int(key[1:])
        keykind = key[0]
        if keyindex not in self.notebuttons.keys():
            return
        if keykind == "d":
            o = sum(j.test_key(k)*v for k,v in self.octavedict.items())
            c = j.axis(4)
            ch = j.axis(5)

            basetune = tones[self.notebuttons[keyindex]]
            make_chord(sh, keyindex, change_tune(basetune,o,c), ch)
        else:
            keyindex = int(key[1:])
            stop_chord(sh, keyindex)

def main():
    print("loading tunes")
    with open("tunes.json") as file:
        songs = json.load(file)
    print("loading instruments")
    with open("instruments.json") as file:
        instr = json.load(file)
    sh = Aplayer(instr[0], 14)
    auto_tune_player(sh, "100:4cccc")
    j = Joystick()
    auto_tune_player(sh, "100:4cccc")
    mode = 3
    instr_index = 0
    modenames = "default", "access"
    scales = [Scale("c"),Scale("g"),Scale("b","quat"),Scale("e","min"),
              Scale("a","min"),Scale("d","min"),Scale("c","penta"),Scale("f")]
    scale = scales[0]
    print("READY")
    for key in j.process():
        if key == "d12":
            z = j.get_axis_pole(1)
            print(z)
            if z >= 0:
                try:
                    s = songs[z]
                except IndexError:
                    s = "100:4+cccccccc"
                auto_tune_player(sh, s)
            else:
                instr_index = (instr_index + 1) % len(instr)
                sh.load_sound(instr[instr_index])
                say("instrument {}".format(instr[instr_index]["name"]))
            continue
        elif key == "d11":
            z = j.get_axis_pole(1)
            print(z)
            if z >= 0:
                scale = scales[z]
            else:
                mode = (mode + 1) % len(modenames)
                say("mode {}".format(modenames[mode]))
            continue
        scale.play_note(sh,j,key,mode)


if __name__ == "__main__":
    main()
