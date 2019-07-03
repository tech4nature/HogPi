import pir
import subprocess

pir_sensor = pir.sensor(14)

while True:
    # if pir_sensor == 1:
    subprocess.run(["python3", "video.py"])
