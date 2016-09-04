__author__ = 'thorvald'

import subprocess as sp
import os

devnull = open(os.devnull, 'wb')


class Aplayer():
    def __init__(self, sound, maxproc=12, gain=15):
        #
        self.processes = [None] * maxproc
        self.gain = gain
        self.load_sound(sound)

    def load_sound(self, sound):
        self.filename = sound["file"]
        self.shift = int(sound["shift"] * 100)
        self.soundname = sound["name"]
        self.start = sound.get("start",0)
        self.lenght = sound.get("length",0)
        self.volume = sound.get("volume",0)

    def play(self, process_id, pitch):
        self.stop(process_id)
        self.processes[process_id] = sp.Popen((tuple(self.get_args(pitch))),
                                              shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)

    def get_args(self,pitch):
        yield "sox"
        yield self.filename
        yield "-d"
        yield from ("pitch", "{:+}".format(pitch * 100 - self.shift))
        yield from ("gain", "{}".format(self.gain + self.volume))
        if self.lenght > 0:
            yield from ("trim", "{}".format(self.start), "{}".format(self.lenght))
        elif self.start > 0:
            yield from ("trim", "{}".format(self.start))
        if self.lenght > 0:
            yield from ("repeat", "{}".format(int(100/self.lenght)))
        else:
            yield from ("repeat", "10")

    def stop(self, process_id):
        if self.processes[process_id] is not None:
            self.processes[process_id].kill()
            self.processes[process_id] = None

    def stop_media(self):
        self.stop(0)

    def play_media(self, filename):
        self.stop(0)
        self.processes[0] = sp.Popen(("sox", filename, "-d", "gain", "0"),
                                     shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
