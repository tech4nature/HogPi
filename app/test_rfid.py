import time
import rfid

new_rfid = rfid.sensor()
while True:
    a = new_rfid.read()
    print(a)
    time.sleep(0.1)
