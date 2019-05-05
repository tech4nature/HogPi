import post
import video
import subprocess
import thermo
import weight

x = input("w = weight \nt = temp \np = post \nv = video \n")

if x == "t":
    temperature = thermo.sensor()
    temperature.write('temp.csv', True)
    temperature.avrg('temp.csv', 'avrtemp.csv', True)

elif x == "v":
    test = subprocess.Popen(['python3', 'video.py'])
    test.wait()

elif x == "w":
    weight_sensor = weight.sensor()
    # weight_sensor.tare_weight()
    weight_sensor.read(True)
    weight_sensor.write('weight.csv', True)
    weight_sensor.avrg('weight.csv', 'avrweight.csv', 0.95, True)
    weight_sensor.tare_weight(100)  # 100 = min tolerance

elif x == "p":
    web = post.http()
    web.post('http://10.172.100.68', 'test', 'test', True)
