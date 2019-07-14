import pir
import subprocess
from datetime import datetime

pir_sensor = pir.sensor(4)

while True:
    hour = int(datetime.strftime('%H'))
    if hour >= 22 and hour <= 6:
        if pir_sensor.read() == 1:
            subprocess.run(["python3", "video.py"])
