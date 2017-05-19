import pyaudio
import wave
import RPi.GPIO as gpio 
gpio.setmode(gpio.BCM) 

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

class ButtonRecorder(object): 
    def __init__(self, filename): 
        self.filename = filename 
        gpio.setup(23, gpio.IN, pull_up_down=gpio.PUD_UP) 
        self.rec = Recorder(channels=2) 

    def start(self): 
        gpio.add_event_detect(23, gpio.FALLING, callback=self.falling, bouncetime=10) 

    def rising(self, channel): 
        gpio.remove_event_detect(23) 
        print 'Button up' 
        gpio.add_event_detect(23, gpio.FALLING, callback=self.falling, bouncetime=10) 
        self.recfile.stop_recording() 
        self.recfile.close() 

    def falling(self, channel): 
        gpio.remove_event_detect(23) 
        print 'Button down' 
        gpio.add_event_detect(23, gpio.RISING, callback=self.rising, bouncetime=10) 
        self.recfile = self.rec.open(self.filename, 'wb')    
        self.recfile.start_recording() 

rec = ButtonRecorder('nonblocking.wav')
rec.start() 

try: 
    raw_input() 

except KeyboardInterrupt: 
    pass 

gpio.cleanup()
