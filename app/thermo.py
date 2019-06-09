from datetime import datetime, timedelta
from time import sleep, strftime
from output import Output
import numpy
import os
import glob

fileRW = Output()


class sensor:
    def __init__(self):
        # Sets up thermostat
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        global base_dir
        global device_folder1
        global device_folder2
        global temp_out
        global temp_in
        global temp_sensors

        base_dir = '/sys/bus/w1/devices/'
        device_folder1 = glob.glob(base_dir + '28*')[0]
        device_folder2 = glob.glob(base_dir + '28*')[1]
        temp_out = device_folder1 + '/w1_slave'
        temp_in = device_folder2 + '/w1_slave'
        temp_sensors = [temp_in, temp_out]

        check = os.path.isfile('/home/pi/avrgtemp_in.csv')  # checks if file exists
        if check == False:
            open("/home/pi/avrgtemp.csv", 'x')  # if not creates file

    def get_time(self, debug=False):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        if debug == True:
            print("Raw time: ", d)
            print("Refined time: ", x)
        return x

    def read_temp_raw(self, sensor):
        # Gets raw data off the thermostat
        f = open(sensor, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read(self, debug=False):
        # Refines the raw data to something readable
        a = []
        for temp_sensor in temp_sensors:
            lines = self.read_temp_raw(temp_sensor)
            t = self.get_time(False)
            while lines[0].strip()[-3:] != 'YES':
                sleep(0.2)
                lines = self.read_temp_raw(temp_sensor)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                tup_temp = (t, temp_sensor, temp_c)
                if debug == True:
                    print("Time: ", t)
                    print("Data and time: ", tup_temp)
                a.append(tup_temp)
        return a

    def write(self, iterations=60, debug=False):
        i = 0
        while i <= iterations/2:  # iterations halved because of the 2 sensors
            data = self.read(debug)
            # if debug == True:
            #     print("Data to write: ", data)
            fileRW.write("/home/pi/temp_in.csv", data[0])
            fileRW.write("/home/pi/temp_out.csv", data[1])
            i += 1

    def avrg(self, readfile, writefile, debug=False):
        times = fileRW.read("/home/pi/" + readfile, 0, debug)
        data = fileRW.read("/home/pi/" + readfile, 2, debug)
        start = times[0]  # 1st time in array
        data_float = numpy.array(data).astype(numpy.float)
        numpy_average = numpy.average(data_float)  # Complete avarage
        numpy_max = numpy.amax(data_float)  # max value of array
        avrgtemp = round(numpy_average, 2)
        tup_temp_refined = (start, avrgtemp)
        fileRW.write("/home/pi/" + writefile, tup_temp_refined)
        # delete file after use to give clean start for next average
        os.remove("/home/pi/" + readfile)
        name = str(readfile.split('.csv')[0]).replace('_', ' ')
        if debug == True:
            print("Average temperature for " + name + " is: ", avrgtemp)
            print("Max temperature for " + name + " is: ", numpy_max)
            print("Conbined data for " + name + " is: ", tup_temp_refined)
        return tup_temp_refined  # posted to http server
