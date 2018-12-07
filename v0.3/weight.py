from hx711 import HX711
from time import sleep, strftime
from datetime import datetime, timedelta


class sensor:
    def __init__(self):
        # Sets up scales
        global hx
        hx = HX711(5, 6)
        hx.set_reading_format("LSB", "MSB")

        hx.reset()
        hx.tare()

    def get_time(self, debug):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        if debug == True:
            print("Raw time: ", d)
            print("Refined time: ", x)
        return x

    def read(self, debug):
        # Gets data off of weight scales
        val = hx.get_weight(5)
        t = sensor.get_time(False)
        tup_weight = (t, val)
        hx.power_down()
        hx.power_up()
        if debug == True:
            print("Time: ", t)
            print("Data: ", val)
            print("Combined: ", tup_weight)
        time.sleep(0.5)
        return tup_weight

    def write(self, filename, debug):
        with open(os.path.dirname(os.path.realpath(__file__)) + filename, 'w+', newline='') as f:
            data = sensor.read(False)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

    def avrg(self, readfile, writefile, debug):
        # declarations
        sum_count = 0  # declare before sum_count
        valid_number = 0  # decalare befors use
        count = True
        with open(os.path.dirname(os.path.realpath(__file__)) + readfile, 'r') as f:
            data = [row[1] for row in reader(f, delimiter=';')]
            times = [row[0] for row in reader(f, delimiter=';')]
            data_refined = np.array(data).astype(np.float)
            # find the mean
            np_average = np.average(data_refined)  # Complete avarage
            np_max = np.amax(data_refined)  # max value of array
            if debug == True:
                print("Average is...", np_average)
                print("Max value is ....", np_max)
            for i in np.nditer(data_refined):
                if (i/np_max) > percentage_of_max:  # only those close to max
                    sum_count = sum_count + i  # count the sum
                    valid_number = valid_number + 1  # count the number
                    if count == True:
                        starttime = datetime.strptime(
                            times[i], '%Y %m %d %H %M %S')  # 1st item in list times
                        count = False
                    if debug == True:
                        print(i)
                else:
                    if debug == True:
                        print("Do not use")
            sp_average = sum_count/valid_number  # gives average of hedgehog
            tup_weight_refined = (starttime, sp_average)
            if debug == True:
                print("The real average is: ", sp_average)
                print("Start time is: ", starttime)
                print("The combined data is: ", tup_weight_refined)
            return tup_weight_refined  # http post this value
