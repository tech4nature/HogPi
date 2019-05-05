import post
import video
import subprocess
import thermo
import weight
import power
import output
import video_ftp
import pir


def main_menu():
    x = input("w = weight \nt = temp \np = post \nv = video \nf = ftp \nr = ftp \n")

    if x == "t":
        temperature = thermo.sensor()
        temperature.write(time=10, debug=True)
        temperature.avrg('temp_in.csv', 'avrtempin.csv', debug=True)
        temperature.avrg('temp_out.csv', 'avrtempout.csv', debug=True)
        main_menu()

    elif x == "v":
        test = subprocess.Popen(['python3', '/home/pi/v0.8/video.py'])
        test.wait()
        test.terminate()
        main_menu()

    elif x == "w":
        weight_sensor = weight.sensor()
        weight_sensor.tare_weight(0.5)
        weight_sensor.read(True)
        weight_sensor.write('weight.csv', 30, True)
        weight_sensor.avrg('weight.csv', 'avrweight.csv', -1, True) # -1 use all values
        # weight_sensor.tare_weight(100)  # 100 = min tolerance
        main_menu()

    elif x == "p":
        web = post.http()
        out = output.Output()
        json_file = out.write_json('The Hedgehog Box of Doom', 'Jack Whitehorn', '65 Horns Road', 'Stroud, Gloucstershire', 'Gl5 1EB', 'OK',
                                   'gaberielbkyne@gmail.com', 'Jack Whitehorn', '01453766796', 1, '2019-01-19T00:00:00.000Z', '0', '0', 51.7429235, -2.2057314)
        web.post("https://hedgehog.bitnamiapp.com/api/boxes", json_file, True)
        main_menu()

    elif x == "f":
        new_ftp = video_ftp.ftp()
        filename = new_ftp.send_video('hog_video', 'ftpk@robotacademy.co.uk',
                                      'Angelgabe23', '/', box_id=1001, hog_id=1234)
        print(filename)
        main_menu()


main_menu()
