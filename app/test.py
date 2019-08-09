import post
import video
import subprocess
import thermo
import weight
import rfid
import pir


def main_menu():
    x = input("temp=t\nvideo=v\nweight=w\nrfid=r\npir=p\npirVerbose=pv\n")

    if x == "t":
        temperature = thermo.sensor()
        temperature.write(time=10)
        temperature.avrg("temp_in.csv", "avrtempin.csv")
        temperature.avrg("temp_out.csv", "avrtempout.csv")
        main_menu()

    elif x == "v":
        test = subprocess.Popen(["python3", "/home/pi/HogPi/app/video.py"])
        test.wait()
        test.terminate()
        main_menu()

    elif x == "w":
        weight_sensor = weight.sensor()
        weight_sensor.tare_weight()
        weight_sensor.read()
        weight_sensor.write("weight.csv", 30)
        weight_sensor.avrg("weight.csv", "avrweight.csv")  # -1 use all values
        # weight_sensor.tare_weight(100)  # 100 = min tolerance
        main_menu()

    elif x == "p":
        '''
        Runs PIR until triggered(1) and then runs pin reverts to not triggered(0)
        '''
        pir_sensor = pir.sensor(11)
        while True:
            result = pir_sensor.read()
            if result == 1:
                print('PIR TRIGGERED')
                while True:
                    result = pir_sensor.read()
                    if result == 0:
                        print('PIR NOT TRIGGERED')
                        break

        main_menu()

    elif x == "pv":
        '''
        Runs PIR until triggered(1) and then runs pin reverts to not triggered(0)
        '''
        pir_sensor = pir.sensor(11)
        while True:
            print(pir_sensor.read())

        main_menu()


main_menu()
