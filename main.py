from input import Joystick
from output import Soundhandler
from collections import namedtuple
from math import floor
from time import sleep

Tune = namedtuple("Tune","letter,octave,change")


def get_tune_idc(tune):
    return \
        {"a": 0, "b": 2, "c": -9, "d": -7, "e": -5, "f": -4, "g": -2}[tune.letter] + \
        tune.octave * 12 + \
        tune.change

def get_frequency(tune):

    return int(440 * 2**(get_tune_idc(tune)/12))

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
    sleep(time*(0.5))
    stop_chord(sh,[tune])

def play_chord(sh,tunes):
    ground = tunes[0]
    for tune in tunes:
        sh.play(ground,get_frequency(tune))


def stop_chord(sh, tunes):
    ground = tunes[0]
    for tune in tunes:
        sh.stop(ground, get_frequency(tune))


def main():
    j = Joystick()
    sh = Soundhandler()
    print("READY")
    while True:
        j.process()
        if j.get_free("b10"):
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("d", 0, 0), 1)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("d", 0, 0), 1)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("f", 0, 0), 1)
            forceplay_tune(sh, Tune("g", 0, 0), 2)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("f", 0, 0), 1)
            forceplay_tune(sh, Tune("g", 0, 0), 2)
            forceplay_tune(sh, Tune("g", 0, 0), 0.5)
            forceplay_tune(sh, Tune("a", 0, 0), 0.5)
            forceplay_tune(sh, Tune("g", 0, 0), 0.5)
            forceplay_tune(sh, Tune("f", 0, 0), 0.5)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("g", 0, 0), 0.5)
            forceplay_tune(sh, Tune("a", 0, 0), 0.5)
            forceplay_tune(sh, Tune("g", 0, 0), 0.5)
            forceplay_tune(sh, Tune("f", 0, 0), 0.5)
            forceplay_tune(sh, Tune("e", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("g", -1, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 2)
            forceplay_tune(sh, Tune("c", 0, 0), 1)
            forceplay_tune(sh, Tune("g", -1, 0), 1)
            forceplay_tune(sh, Tune("c", 0, 0), 2)




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






