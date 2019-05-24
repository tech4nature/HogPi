import time
import rfid

new_rfid = rfid.sensor()
while True:
    a = new_rfid.read()
    print('this is a value read by rfid' + a)
    time.sleep(0.1)
