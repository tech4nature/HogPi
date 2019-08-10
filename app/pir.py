# from RPi import GPIO
import RPi
import time
import logging


logger = logging.getLogger(__name__)


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
        result = RPi.GPIO.input(pin)
        #logger.debug("Read value %s from pin %s", result, pin)
        if result == 1:
            logger.debug("PIR Triggered")
        return result
