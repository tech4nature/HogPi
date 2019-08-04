import led
import pir
import video

def main_menu():
    x = input("video=v\npir=p\nled=l\n")

    if x == "v":
        test = subprocess.Popen(["python3", "/home/pi/HogPi/app/remoteCam/video.py"])
        test.wait()
        test.terminate()
        main_menu()

    elif x == "p":
        '''
        Runs PIR until triggered(1) and then runs pin reverts to not triggered(0)
        '''
        pir_sensor = pir.sensor(4)
        while True:
            result = pir_sensor.read()
            if result == 1:
                print('PIR TRIGGERED')
                while True:
                    result = pir_sensor.read()
                    if result == 0:
                        print('PIR NOT TRIGGERED')
                        break
                break
        main_menu()

    elif x == 'l':
        irled = led.sensor(3)  # Instantiate led class and assign the pin the BCM3
        print('LED ON')
        irled.on()  # Turn led off
        print('LED OFF')
        irled.off()
        main_menu()


main_menu()
