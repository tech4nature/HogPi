import led
import time

irled = led.sensor(3)  # Instantiate led class and assign the pin the BCM17
while True:
    time.sleep(2)
    irled.on()  # Turn led on
    time.sleep(2)
    irled.off()