import pyaudio
import numpy as np
import time
import threading


fs = 8000
volume = 1.0


def get_start(beginstrenght,endstrenght,ticks,fadeframes):
    return beginstrenght + np.minimum(np.arange(ticks),np.ones((ticks,))*fadeframes).astype(np.float32)/fadeframes * (endstrenght - beginstrenght)



class Soundhandler():
    def __init__(self):
        print("Setup output device")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=fs,
                                  output=True,
                                  stream_callback=self.callback)
        self.stream.frames_per_buffer = 1024
        self.w = open("test.txt","w")

        self.freqlist = set() #contains tuples: id,freq
        self.freqprev = set()
        self.index = 0
        self.next_wave = []
        self.soundupdateThread = threading.Thread(None,self.update_next_wave)
        self.soundupdateThread.start()
        print("Output ready")

    def update_next_wave(self):
        while True:
            self.next_wave = get_next_data(1024)
    def get_next_data(self, ticks, fadeframes=fs/20):
        self.index += ticks
        try:
            prevvol = 0.9/len(self.freqprev)
        except ZeroDivisionError:
            prevvol = 0
        try:
            nowvol = 0.9 / len(self.freqlist)
        except ZeroDivisionError:
            nowvol = 0

        for id_,freq in self.freqlist | self.freqprev:
            now = (id_,freq) in self.freqlist
            prev = (id_,freq) in self.freqprev
            fade = prev and not now
            rase = now and not prev
            start = get_start(prevvol *(not rase),nowvol*(not fade),ticks,fadeframes)

            yield (np.sin(2 * np.pi * (np.arange(ticks) + self.index) * freq / fs) * start * min(1,(220/freq)**2)).astype(np.float32)
        self.freqprev = self.freqlist.copy()
    def callback(self, in_data, frame_count, time_info, status):
        print(frame_count)
        fulldata = list(self.next_wave)
        if fulldata:
            data = sum(fulldata)
        else:
            data = ((np.arange(frame_count)) * 0).astype(np.float32)
        #self.w.write(str(list(data))+"\n")

        return data, pyaudio.paContinue

    def finish(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.w.close()

    def play(self,*freqid_):
        #self.freqlist = {f for f in self.freqlist if f[0] != freqid_[0]}
        self.freqlist.add(freqid_)

    def stop(self,*freqid_):

        self.freqlist = {f for f in self.freqlist if f[0] != freqid_[0]}


if __name__ == "__main__":
    s = Soundhandler()
    for i in range(10):

        time.sleep(1)
        s.play(i*20+400)
        time.sleep(1)
        s.stop()
    #s.finish()

