import led
import time

irled = led.sensor(11)  # Instantiate led class and assign the pin 
while True:
    time.sleep(2)
    irled.on()  # Turn led on
    print ("LED ON")
    time.sleep(2)
    irled.off()
    print("LED OFF")
