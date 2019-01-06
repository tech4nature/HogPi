import post
import video
import subprocess
import thermo
import weight
import power

def main_menu():
    x = input("w = weight \nt = temp \np = post \nv = video \n")

    if x == "t":
        temperature = thermo.sensor()
        temperature.write('temp.csv', True)
        temperature.avrg('temp.csv', 'avrtemp.csv', True)
        main_menu()

    elif x == "v":
        test = subprocess.Popen(['python3', 'video.py'])
        test.wait()
        main_menu()

    elif x == "w":
        weight_sensor = weight.sensor()
        weight_sensor.tare_weight(0.6)
        weight_sensor.read(True)
        weight_sensor.write('weight.csv', True)
        weight_sensor.avrg('weight.csv', 'avrweight.csv', 0.95, True)
        # weight_sensor.tare_weight(100)  # 100 = min tolerance
        main_menu()

    elif x == "p":
        web = post.http()
        web.post('http://10.172.100.68', 'test', 'test', True)
        main_menu()
