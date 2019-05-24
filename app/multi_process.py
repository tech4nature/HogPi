from multiprocessing import Process, current_process
import rfid
import test
import thermo


def read_rfid():
    a = new_rfid.read()
    print(a)
    time.sleep(0.1)


def temp():
    temperature = thermo.sensor()
    temperature.write(time=10, debug=True)
    temperature.avrg('temp_in.csv', 'avrtempin.csv', debug=True)
    temperature.avrg('temp_out.csv', 'avrtempout.csv', debug=True)


q = multiprocessing.Queue()
p1 = multiprocessing.Process(target=read_rfid, args=(q,))
p2 = multiprocessing.Process(target=temp, args=(q,))
p1.start()
p2.start()
p1.join()
p2.join()
