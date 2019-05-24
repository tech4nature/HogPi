import subprocess
from datetime import datetime
import time
import os
import sys
import led

irled = led.sensor(17)
while True:

    print('on')  # Instantiate led class and assign the pin the BCM17
    irled.on()  # Turn led on
    time.sleep(5)
    print('off')
    irled.off()  # Turn led off
    time.sleep(5)
