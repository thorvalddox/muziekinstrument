import pyaudio
import numpy as np
import time
import threading





volume = 1.0


def get_start(beginstrenght,endstrenght,ticks,fadeframes):

    return beginstrenght + np.minimum(np.arange(ticks),np.ones((ticks,))*fadeframes).astype(np.float32)/fadeframes * (endstrenght - beginstrenght)



class Soundhandler():
    def __init__(self,fs):
        print("Setup output device")
        self.fs = fs
        self.index = 0
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.fs,
                                  output=True)

        self.freqlist = set() #contains tuples: id,freq
        self.freqprev = set()
        self.prevtime = 0

        self.invoketime = 0


        self.bufferer = threading.Thread(None,self.add_to_buffer)
        self.bufferer.start()
        print("Output ready")

    def update_next_wave(self):
        self.next_wave = get_next_data(1024)
    def get_next_data(self, ticks, invoke, fadetime=1/16):
        pass
        """
        self.prevtime = self.invoketime
        self.invoketime = invoke
        ticklen = self.fs * (self.invoketime - self.prevtime)
        self.index += ticklen

        fadeframes = self.fs*fadetime
        #print("lost:",ticklen - ticks,"frames")

        try:
            prevvol = 0.9/len(self.freqprev)
        except ZeroDivisionError:
            prevvol = 0
        try:
            nowvol = 0.9 / len(self.freqlist)
        except ZeroDivisionError:
            nowvol = 0
        """
        for id_,freq in self.freqlist | self.freqprev:
            """
            now = (id_,freq) in self.freqlist
            prev = (id_,freq) in self.freqprev
            fade = prev and not now
            rase = now and not prev
            start = get_start(prevvol *(not rase),nowvol*(not fade),ticks,fadeframes)
            """
            start = 1.0
            yield (np.sin(2 * np.pi * (np.arange(ticks) + self.index) * freq / self.fs) * start * min(1,(220/freq)**2)).astype(np.float32)
        self.freqprev = self.freqlist.copy()
    def callback(self, in_data, frame_count, time_info, status):
        data = get_new_data_list(frame_count,time_info["output_buffer_dac_time"])

        return data, pyaudio.paContinue

    def get_new_data_list(self,ticks,invoke):
        fulldata = list(self.get_next_data(ticks,invoke))

        if fulldata:
            return sum(fulldata)
        else:
            return ((np.arange(ticks)) * 0).astype(np.float32)


    def add_to_buffer(self):
        buffersize=self.fs
        self.starttime = time.time()
        previndex = 0
        while True:
            maxindex = (time.time() - self.starttime)*self.fs + buffersize
            self.stream.write(self.get_new_data_list(maxindex - previndex,maxindex-previndex))
            print("{:>8.2} {:>8.2} {:>8.2} {:>8.2".format(maxindex - previndex,maxindex,maxindex/self.fs,(time.time() - self.starttime))
            previndex = maxindex
            time.sleep(0.05)


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
        s.play(0, i*20+400)
        time.sleep(1)
        s.stop(0)
        time.sleep(1)
    s.finish()

