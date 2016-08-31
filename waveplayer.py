
import pyaudio
import wave
import threading
import numpy

CHUNK = 1024
class WavePlayer():
    def __init__(self,filename):
        self.wf = wave.open(filename, 'rb')

        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        # open stream (2)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)

        # read data
        self.data = self.wf.readframes(CHUNK)
        print(self.data)
        self.active = True

        self.playthread = threading.Thread(None,self.play)
        self.playthread.run()
    def play(self):
        # play stream (3)
        while len(self.data) and self.active:
            self.stream.write(self.data)
            self.data = self.wf.readframes(CHUNK)
    def stop(self,wait=False):
        self.active = wait
        self.playthread.join(None)
        # stop stream (4)
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio (5)
        self.p.terminate()
    def wait(self):
        self.stop(True)

if __name__ == "__main__":
    p = WavePlayer("hobbit.wav")
    p.play()
    p.wait()
