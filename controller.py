import RPi.GPIO as GPIO
import time
from subprocess import call
import subprocess
from viz import *

gpio.setmode(GPIO.BCM)

class ButtonRecorder(pin): 
	def __init__(self, pin):
		self.pin = pin
		print(self.pin)
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def start(self): 
		while True:
			input_state = GPIO.input(self.pint)
			if input_state == False:
				print("Say something! (:")
				subprocess.Popen(["python","/home/pi/Desktop/waves/killer.py"])
				print("Recording now")
				call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])
				print("Recording stopped")
				createViz(self.pin)  
				print("Viz Created")

rec = ButtonRecorder(23)
rec.start() 

# while True:
#     input_state = GPIO.input(23)
#     if input_state == False:
#     	print("Say something! (:")
#     	subprocess.Popen(["python","/home/pi/Desktop/waves/killer.py"])
# # 	print("Recording now")
# #         call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])
# # 	print("Recording stopped")
# 	# subprocess.Popen(["python","/home/pi/Desktop/waves/viz.py"]) 
# # 	createViz()       
# #         #launch printer.py
# # 	print("Viz stopped")
# #         time.sleep(0.2)
