import post
import video
import subprocess
import thermo
import weight
import power
import output

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
        out = output.Output()
        json_file = out.write_json('The Hedgehog Box of Doom', 'Jack Whitehorn', '65 Horns Road', 'Stroud, Gloucstershire', 'Gl5 1EB', 'OK', 'gaberielbkyne@gmail.com', 'Jack Whitehorn', '01453766796', 1, '2019-01-19T00:00:00.000Z', '0', '0', 51.7429235, -2.2057314)
        web.post("https://hedgehog.bitnamiapp.com/api/boxes", json_file, True)
        main_menu()


main_menu()
