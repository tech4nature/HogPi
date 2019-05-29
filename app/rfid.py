import serial
from time import sleep

timeout = 1
global TagFound
global tag
TagFound = None
tag = None


class sensor:
    def __init__(self):
        global ser
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=10
        )
        # ser.write(b'SD2\r\n') # Sets transponder default to FDX-B(animal tag)

    def read(self):
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b'sd2\r\n')
        a = ser.read_until(size=19).decode('utf-8')
        print(a)
        if len(a) < 16:
            return 'TagNotPresent'
        else:
            return a
