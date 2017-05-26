import RPi.GPIO as GPIO
import time
from subprocess import call
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(23)
    if input_state == False:
    	print("Say something! (:")
    	subprocess.Popen(["python","/home/pi/Desktop/waves/killer.py"])
	print("Recording now")
        call(["arecord","/home/pi/Desktop/waves/audio3.mp3", "-D", "sysdefault:CARD=1"])
	print("Recording stopped")
	subprocess.Popen(["python","/home/pi/Desktop/waves/viz.py"])        
        #launch printer.py
	print("Viz stopped")
        time.sleep(0.2)
