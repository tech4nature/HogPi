import pir
import subprocess
from datetime import datetime
import led
import json
from json_minify import json_minify

config = json.loads(
    json_minify(open("config.json").read())
)  # Removes comments from JSON then loads into python dictionaryjw

pir_sensor = pir.sensor(config["pirPin"])
irled = led.sensor(
    config["ledPin"]
)  # Instantiate led class and assign the pin the BCM3
irled.off()  # Turn led off


while True:
    hour = int(datetime.strftime(datetime.now(), "%H"))
    #   if hour > 0: # switch on for commissioning
    if config["remoteCam"] == True:
        if hour >= config["minTime"] or hour <= config["maxTime"]:
            if pir_sensor.read(config["requiredPirIterations"]) == 1:
                print("PIR triggered")
                irled.on()
                subprocess.run(
                    ["/usr/bin/python3", "/home/pi/HogPi/app/remoteCam/video.py"]
                )
                irled.off()
    if config["rfidTunnel"] == True:
        pass  # RFID Tunnel code to go here
