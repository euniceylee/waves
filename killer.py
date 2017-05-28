import RPi.GPIO as GPIO
import time
import sys
from subprocess import call

GPIO.setmode(GPIO.BCM)

pin = int(sys.argv[1])

GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(pin)
    if input_state == True:
        call(["killall", "-KILL", "arecord"])
        break
