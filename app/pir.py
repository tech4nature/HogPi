import RPi.GPIO as GPIO
import time


class sensor:

    def __init__(self):
        time.sleep(2)  # set up of PIR reader
        GPIO.setmode(GPIO.BCM)  # set mode

    def read(self, pin):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set the PIR to pin  8
        return GPIO.input(pin)
