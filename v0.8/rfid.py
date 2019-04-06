import serial
from time import sleep


class rfid_sensor:
    def __init__(self):
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
        )

        ser.write(b'SD2\r\n')
        ser.read(3)

    def read(self):
        return ser.read(17).decode('utf-8').split('''\r''')[0]
