import serial

'''s = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0,
)'''

with serial.serial_for_url('spy:///dev/ttyUSB0?file=test.txt', timeout=1) as s:
    s.dtr = False
    s.write(b'rat\r\n')
    s.read(20)
    s.dtr = True
    s.write(serial.to_bytes(range(256)))
    s.read(400)
    s.send_break()
    with open('test.txt') as f:
        print(f.read())
