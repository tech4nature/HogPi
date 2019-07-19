import video
import subprocess
import thermo
import weight
import rfid
import pir


def main_menu():
    x = input("temp=t\nvideo=v\nweight=w\nrfid=r\npir=p\n")

    if x == "t":
        temperature = thermo.sensor()
        temperature.write(iterations=10, debug=True)
        temperature.avrg("temp_in.csv", "avrtempin.csv", debug=True)
        temperature.avrg("temp_out.csv", "avrtempout.csv", debug=True)
        main_menu()

    elif x == "v":
        test = subprocess.Popen(["python3", "/home/pi/HogPi/app/video.py"])
        test.wait()
        test.terminate()
        main_menu()

    elif x == "w":
        weight_sensor = weight.sensor()
        weight_sensor.tare_weight(0.5)
        weight_sensor.read(True)
        weight_sensor.write("weight.csv", 30, True)
        weight_sensor.avrg("weight.csv", "avrweight.csv", -1, True)  # -1 use all values
        # weight_sensor.tare_weight(100)  # 100 = min tolerance
        main_menu()

    elif x == "r":
        rfid_sensor = rfid.sensor()
        rfid_sensor.read()
        main_menu()

    elif x == "p":
        pir_sensor = pir.sensor(11)
        pir_sensor.read()
        main_menu()


main_menu()
