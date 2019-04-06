import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)  # set mode
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set the PIR to pin  8

try:
    time.sleep(2)

    while True:
        if GPIO.input(11):
            print("Pin 11 is HIGH")
        else:
            print("Pin 11 is LOW")
        time.sleep(0.3)

except KeyboardInterrupt:
    print('cleaning')
    GPIO.cleanup()
