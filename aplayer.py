__author__ = 'thorvald'

import subprocess as sp


class Aplayer():
    def __init__(self,soundname,maxproc=12):
        #http://soundbible.com/1437-Kettle-Whistle.html
        self.processes = [None]*maxproc
        self.soundname = soundname
    def play(self,process_id,pitch):
        self.processes[process_id] = sp.Popen(("sox",self.soundname,"-d","pitch","{:+}".format(pitch*100-800)))
    def stop(self,process_id):
        if self.processes[process_id] is not None:
            self.processes[process_id].kill()
            self.processes[process_id] = None

