import RPi.GPIO as GPIO
import time
from subprocess import call
import subprocess
from viz import *

GPIO.setmode(GPIO.BCM)

class ButtonRecorder: 
	def __init__(self, pin):
		self.pin = pin
		print(self.pin)
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.input_state = GPIO.input(self.pin)
	
	def getInputState(self):
		input_state = GPIO.input(self.pin)
		return input_state

	def start(self): 
		print("Say something! (:")
		subprocess.Popen(["python","/home/pi/Desktop/waves/killer.py"])
		print("Recording now")
		call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])
		print("Recording stopped")
		createViz(self.pin)  
		print("Viz Created")


rec23 = ButtonRecorder(23)
s23 = rec23.getInputState()

rec24 = ButtonRecorder(24)
s24 = rec24.getInputState()

while True:
	if (s23 == False):
		rec23.start()
	elif (s24 == False):
		rec24.start()