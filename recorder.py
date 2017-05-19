import RPi.GPIO as gpio 
from recorder import Recorder 
gpio.setmode(gpio.BCM)  

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
