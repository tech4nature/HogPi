import video
import subprocess
import thermo
import weight
import rfid
import pir
from data import Data


weight_sensor: weight.Sensor = weight.Sensor()


def main_menu():
    x = input(
        "temp=t\nvideo=v\nweight=w\ntareWeight=tw\nrfid=r\npir=p\npirVerbose=pv\n"
    )

    if x == "t":
        temperature = thermo.sensor()
        t1 = temperature.write(iterations=30)
        print(t1)
        print(temperature.avrg("temp_in.csv", "avrtempin.csv"))
        print(temperature.avrg("temp_out.csv", "avrtempout.csv"))
        main_menu()

    elif x == "v":
        test = subprocess.Popen(["python3", "/home/pi/HogPi/app/video.py"])
        test.wait()
        test.terminate()
        main_menu()

    elif x == "w":
        data: Data = weight_sensor.read()
        data: Data = weight_sensor.avrg(data)
        print(data.value)
        main_menu()

    elif x == "tw":
        weight_sensor.tare_weight()
        main_menu()

    elif x == "p":
        """
        Runs PIR until triggered(1) and then runs pin reverts to not triggered(0)
        """
        pir_sensor = pir.sensor(11)
        while True:
            result = pir_sensor.read()
            if result == 1:
                print("PIR TRIGGERED")
                while True:
                    result = pir_sensor.read()
                    if result == 0:
                        print("PIR NOT TRIGGERED")
                        break

        main_menu()

    elif x == "pv":
        """
        Runs PIR until triggered(1) and then runs pin reverts to not triggered(0)
        """
        pir_sensor = pir.sensor(11)
        while True:
            print(pir_sensor.read())

        main_menu()


main_menu()
