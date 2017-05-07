import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
    	print("Say something! (:")
    	#launch killer.py
        call(["arecord","/home/pi/Desktop/waves/audio.mp3", "-D", "sysdefault:CARD=1"])
        call(["python","/home/pi/Desktop/waves/viz.py"])
        #launch printer.py
        time.sleep(0.2)