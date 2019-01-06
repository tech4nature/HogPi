from hx711 import HX711
from time import sleep, strftime
from datetime import datetime, timedelta
from csv import reader, writer
import numpy
import os


class sensor:
    def __init__(self):
        # Sets up scales
        global hx
        self.No_Tare = False
        hx = HX711(5, 6)
        hx.set_reading_format("LSB", "MSB")
        hx.set_reference_unit(391)  # 391
        hx.reset()
        hx.tare()

        check = os.path.isfile('/home/pi/weight.csv')  # checks if file exists
        if check == False:
            open("/home/pi/weight.csv", 'x')  # if not creates file
        check = os.path.isfile('/home/pi/tare_weight.csv')  # checks if file exists
        if check == False:
            open("/home/pi/tare_weight.csv", 'x')  # if not creates file

    def tare_weight(self, decimal_of_max):
        # checks if weight.csv exists and is non-empty
        if os.path.isfile('/home/pi/weight.csv') and os.path.getsize('/home/pi/weight.csv') > 0:
            with open('/home/pi/weight.csv', 'r') as r_csvfile:
                data_reader = reader(r_csvfile, delimiter=',')
                data = []
                for row in data_reader:
                    data.append(row[1])
                a = numpy.array(data).astype(numpy.float)
        print("this is last value to use as a[-1]", a[-1])
        # test if the last value is below 90% retare weight
        if a[-1] > decimal_of_max*numpy.amax(a) and a[-1] > 100:
            # set flag to allow no tare
            self.No_Tare = True
            print("Set this if you do not want a tare")
        else:
            # set flag to allow tare
            self.No_Tare = False
            print("Set this if you  WANT a tare")
        return

    def get_time(self, debug):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        if debug is True:
            print("Raw time: ", d)
            print("Refined time: ", x)
        return x

    def read(self, debug):
        # Gets data off of weight scales
        if self.No_Tare is False:
            # tare weight unless set to true
            val = hx.get_weight(5)
        else:
            # Do not tare weight but use stored value
            val = hx.get_weight_no_tare(5)
        # reslove zero values for negatives
        if val < 0:
            val = 0
        t = self.get_time(False)
        tup_weight = (t, val)
        hx.power_down()
        hx.power_up()
        if debug is True:
            print("Time: ", t)
            print("Data: ", val)
            print("Combined: ", tup_weight)
        sleep(0.5)
        return tup_weight

    def write(self, filename, debug):
        with open('/home/pi/' + filename, 'w', newline='') as f:
            data_writer = writer(f)
            i = 0
            while i <= 10:
                data = self.read(debug)
                if debug == True:
                    print("Data to write: ", data)
                data_writer.writerow(data)
                i += 1

    def avrg(self, readfile, writefile, percentage_of_max, debug):
        # declarations
        sum_count = 0  # declare before sum_count
        valid_number = 0  # decalare before use to avoid negative division
        count = True
        start = []  # declare before use to avoid undeclared error
        starttime = ""  # declare before use to avoid undeclared error
        with open("/home/pi/" + readfile, 'r') as f:
            data_reader = reader(f, delimiter=',')
            times = []
            data = []
            for row in data_reader:
                times.append(row[0])
                data.append(row[1])
            data_array = numpy.array(data).astype(numpy.float)
            # find the mean
            numpy_average = numpy.average(data_array)  # Complete avarage
            numpy_max = numpy.amax(data_array)  # max value of array
            if debug == True:
                print("Average is...", numpy_average)
                print("Max value is ....", numpy_max)
            j = 0
            # avoids zero division
            if numpy_max == 0:
                numpy_max = 0.1
            for i in numpy.nditer(data_array):  # why data array when data is list ??
                if (i/numpy_max) > percentage_of_max:  # only those close to max
                    sum_count = sum_count + i  # count the sum
                    valid_number = valid_number + 1  # count the number
                    if count == True:  # need to get index of i then lookup timestamp
                        start = times[j]
                        starttime = datetime.strptime(
                            start, '%Y %m %d %H %M %S')  # 1st item in list times
                        count = False
                    if debug == True:
                        print(i)
                else:
                    if debug == True:
                        print("Do not use")
                j += 1
            if valid_number == 0:
                # check for zero division
                valid_number = 1
            # calculate averages
            sp_average = sum_count/valid_number  # gives average weight of hedgehog
            tup_weight_refined = (start, sp_average)
            if debug == True:
                print(sum_count)
                print(valid_number)
                print("The real average is: ", sp_average)
                print("Start time is: ", starttime)
                print("The combined data is: ", tup_weight_refined)
            return tup_weight_refined  # http post this value
