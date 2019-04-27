import serial
from time import sleep


class sensor:
    def __init__(self):
        global ser
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0,
        )
        # ser.write(b'SD2\r\n')

    def read(self):
        # ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(b'rat\r\n')
        a = ser.read(34).decode('utf-8')
        if '?1' in a:
            return 'TagNotPresent'

        else:
            a = str(a)  # change to a proper string
            a = a[0:16]  # just send unique data part withou error code
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            return a
