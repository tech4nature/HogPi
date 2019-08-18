import RPi.GPIO as GPIO
import time


class sensor:
    def __init__(self, pin_num):
        global pin
        pin = pin_num
        time.sleep(2)  # set up of PIR reader
        GPIO.setmode(GPIO.BCM)  # set mode
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read(self, iterations=300):
        # logger.debug("Read value %s from pin %s", RPi.GPIO.input(pin), pin)
        value = 0
        for i in range(iterations):  # sample iteration times
            if GPIO.input(pin) == 1:  # count the positive reads
                value = value + 1
                print(value)  # leave in for commissioning
                print(iterations)  # leave in for commissioning
            if value == iterations:  # if all positive then return 1
                return 1
