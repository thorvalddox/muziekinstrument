from input import Joystick
from output import Soundhandler
from collections import namedtuple
from math import floor
from time import sleep

Tune = namedtuple("Tune","letter,octave,change")

def get_frequency(tune):
    diff_from_A4 = \
        {"a":0,"b":2,"c":-9,"d":-7,"e":-5,"f":-4,"g":-2}[tune.letter] + \
        tune.octave * 12 + \
        tune.change
    return int(440 * 2**(diff_from_A4/12))


def all_tunes(low,high):
    for o in range(low,high+1):
        for t in "acdefg":
            for c in [-1,0,1]:
                yield Tune(t,o,c)

def forceplay_tune(sh,tune,time):
    sh.play((tune, get_frequency(tune)))
    sleep(time*(0.5))
    sh.stop((tune, get_frequency(tune)))

def main():
    j = Joystick()
    sh = Soundhandler()
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
                sh.stop((t,get_frequency(t)))
            elif not j.get_free({"c":"b1","d":"b2","e":"b3","f":"b4","g":"b6","a":"b8"}[t.letter]):
                sh.stop((t,get_frequency(t)))
            elif t.change != j.get_hat(0,True) - j.get_hat(0,False):
                sh.stop((t, get_frequency(t)))
            else:
                sh.play((t, get_frequency(t)))






if __name__ == "__main__":
    main()






