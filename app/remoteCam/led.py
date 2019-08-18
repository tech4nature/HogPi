from gpiozero import LED


class sensor:
    def __init__(self, pin):
        self.led = LED(pin)
        return

    def on(self, value=1):
        self.led.on()  # Full brightness unless told otherwise
        return

    def off(self):
        self.led.off()  # Off
        return
