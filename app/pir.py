# from RPi import GPIO
import RPi
import time


class sensor:
    def __init__(self, pin_num):
        global pin
        pin = pin_num
        time.sleep(2)  # set up of PIR reader
        RPi.GPIO.setmode(RPi.GPIO.BCM)  # set mode
        RPi.GPIO.setup(
            pin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN
        )  # Set the PIR to pin 8

    def read(self):
        print(RPi.GPIO.input(pin))
        return RPi.GPIO.input(pin)
