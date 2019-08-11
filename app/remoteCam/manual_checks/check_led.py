import led
import time

irled = led.sensor(3)  # Instantiate led class and assign the pin the BCM5
while True:
    time.sleep(2)
    irled.on()  # Turn led on
    print("LED ON")
    time.sleep(2)
    irled.off()
    print("LED OFF")
