import RPi.GPIO as GPIO
import time
from gpiozero import PWMLED

led = PWMLED(17)
while True:
    led.value = 1
    print("on")
    time.sleep(10)
    led.value = 0
    print("off")
    time.sleep(10)

"""
while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    print("LED on")
    GPIO.output(17, GPIO.HIGH)
    time.sleep(10)
    print("LED off")
    GPIO.output(17, GPIO.LOW)
    time.sleep(10)
"""
# LED test
