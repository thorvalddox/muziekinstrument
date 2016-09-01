__author__ = 'thorvald'

import subprocess as sp
import os

devnull = open(os.devnull, 'wb')


class Aplayer():
    def __init__(self, sound, maxproc=12, gain=30):
        #
        self.processes = [None] * maxproc
        self.load_sound(sound)

    def load_sound(self, sound):
        self.filename = sound["file"]
        self.shift = int(sound["shift"] * 100)
        self.soundname = sound["name"]

    def play(self, process_id, pitch):
        self.stop(process_id)
        self.processes[process_id] = sp.Popen(("sox", self.filename, "-d",
                                               "pitch", "{:+}".format(pitch * 100 - self.shift),
                                               "gain", "30"),
                                              shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)

    def stop(self, process_id):
        if self.processes[process_id] is not None:
            self.processes[process_id].kill()
            self.processes[process_id] = None

    def stop_media(self):
        self.stop(0)

    def play_media(self, filename):
        self.stop(0)
        self.processes[0] = sp.Popen(("sox", filename, "-d", "gain", "30"),
                                     shell=False, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
