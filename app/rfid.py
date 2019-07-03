import serial
from time import sleep

timeout = 1
global TagFound
global tag
TagFound = None
tag = None

# docs: http://www.priority1design.com.au/rfidrw-e-ttl.pdf


class sensor:
    def __init__(self):
        global ser
        ser = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=10,
        )

    def read(self):
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b"sd2\r\n")
        a = ser.read_until(size=19).decode(
            "utf-8"
        )  # 16 byte tag + \r + \n somehow is 19 not 18
        print(a)
        if len(a) < 16:
            return "TagNotPresent"
        else:
            return a
