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
    modenames = "default", "spread", "close", "access"

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
        elif key == "d9":
            mode = (mode + 1) % len(modenames)
            say("mode {}".format(modenames[mode]))

        elif key == "d10":
            instr_index = (instr_index + 1) % len(instr)
            sh.load_sound(instr[instr_index])
            say("instrument {}".format(instr[instr_index]["name"]))

        if mode == 0:
            if key in "d1,d2,d3,d4,d6,d8":
                o = j.test_key(5) - j.test_key(7)
                c = j.axis(4)
                ch = j.axis(5)
                keyindex = int(key[1:])
                l = " cdef g a"[keyindex]
                make_chord(sh, keyindex, Tune(l, o, c), ch)
            elif key in "u1,u2,u3,u4,u6,u8":
                keyindex = int(key[1:])
                stop_chord(sh, keyindex)
        if mode == 1:
            if key in "d1,d2,d3,d4":
                o = j.test_key(5) - j.test_key(7) + j.test_key(6) * 3 - 3 * j.test_key(8)
                c = j.axis(4) + (key == "d4")
                ch = j.axis(5)
                keyindex = int(key[1:])
                l = " bdfg"[keyindex]
                make_chord(sh, keyindex, Tune(l, o, c), ch)
            elif key in "u1,u2,u3,u4":
                keyindex = int(key[1:])
                stop_chord(sh, keyindex)
        if mode == 3:
            if key in "d1,d2,d3,d4,d6,d8":
                o = j.test_key(5) - j.test_key(7)
                c = j.axis(4)
                ch = j.axis(5)
                keyindex = int(key[1:])
                l = " defa c g"[keyindex]
                make_chord(sh, keyindex, Tune(l, o, c), ch)
            elif key in "u1,u2,u3,u4,u6,u8":
                keyindex = int(key[1:])
                stop_chord(sh, keyindex)


if __name__ == "__main__":
    main()
