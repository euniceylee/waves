import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == True:
        call(["killall", "-KILL", "arecord"])
        break