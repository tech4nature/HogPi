# from RPi import GPIO
import RPi.GPIO as GPIO
import time


class sensor:
    def __init__(self, pin_num):
        global pin
        pin = pin_num
        time.sleep(2)  # set up of PIR reader
        GPIO.setmode(GPIO.BCM)  # set mode
        GPIO.setup(
            pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN
        )  # Set the PIR to pin 8

    def read(self):
        # print(GPIO.input(pin))
        return GPIO.input(pin)
