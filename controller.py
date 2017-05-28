import RPi.GPIO as gpio
import time
from subprocess import call
import subprocess
from viz import *

gpio.setmode(GPIO.BCM)

class ButtonRecorder(pin): 
	def __init__(self, pin): 
		self.pin = pin
		print(self.pin)
        gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP) 

    def start(self): 
        gpio.add_event_detect(self.pin, gpio.FALLING, callback=self.falling, bouncetime=10) 

    def rising(self, channel): 
        gpio.remove_event_detect(self.pin) 
        print 'Button up' 
        gpio.add_event_detect(self.pin, gpio.FALLING, callback=self.falling, bouncetime=10) 
		print("Recording stopped")
		call(["killall", "-KILL", "arecord"])
		createViz(self.pin)   

    def falling(self, channel): 
		print(self.pin)
        gpio.remove_event_detect(self.pin) 
        print 'Button down' 
        gpio.add_event_detect(self.pin, gpio.RISING, callback=self.rising, bouncetime=10) 
		print("Recording now")
        call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])

rec = ButtonRecorder(23)
rec.start() 

# while True:
#     input_state = GPIO.input(23)
#     if input_state == False:
#     	print("Say something! (:")
#     	subprocess.Popen(["python","/home/pi/Desktop/waves/killer.py"])
# 	print("Recording now")
#         call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])
# 	print("Recording stopped")
# 	# subprocess.Popen(["python","/home/pi/Desktop/waves/viz.py"]) 
# 	createViz()       
#         #launch printer.py
# 	print("Viz stopped")
#         time.sleep(0.2)
