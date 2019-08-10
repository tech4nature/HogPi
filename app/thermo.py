from datetime import datetime, timedelta
from datetime import timezone
from time import sleep, strftime
from output import Output
import numpy
import os
import glob
import logging

fileRW = Output()


logger = logging.getLogger(__name__)


class sensor:
    def __init__(self):
        # Sets up thermostat
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-therm")

        global base_dir
        global temp_sensors
        global num_t_sensor
        temp_sensors = []
        base_dir = "/sys/bus/w1/devices/"
        for i in glob.glob(base_dir + "28*"):
            temp_sensors.append(i + "/w1_slave")
        num_t_sensor = len(temp_sensors)
        if num_t_sensor == 0:
            raise Exception

    def get_time(self):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        logger.debug("Raw time: %s", d)
        logger.debug("Refined time: %s", x)
        return x

    def read_temp_raw(self, sensor):
        # Gets raw data off the thermostat
        f = open(sensor, "r")
        lines = f.readlines()
        f.close()
        return lines

    def read(self):
        # Refines the raw data to something readable
        a = []
        for temp_sensor in temp_sensors:
            lines = self.read_temp_raw(temp_sensor)
            t = self.get_time()
            while lines[0].strip()[-3:] != "YES":
                sleep(0.2)
                lines = self.read_temp_raw(temp_sensor)
            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos + 2 :]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                tup_temp = (t, temp_sensor, temp_c)
                logger.debug("Time: %s", t)
                logger.debug("Data and time: %s", tup_temp)
                a.append(tup_temp)
        return a

    def write(self, iterations=60):
        i = 0
        while i <= iterations / 2:  # iterations halved because of the 2 sensors
            data = self.read()
            fileRW.write("/home/pi/temp_in.csv", data[0])
            if num_t_sensor == 2:
                fileRW.write("/home/pi/temp_out.csv", data[1])
            i += 1

    def avrg(self, readfile, writefile):
        if num_t_sensor == 1 and readfile == "temp_out.csv":
            return None
        times = fileRW.read("/home/pi/" + readfile, 0)
        data = fileRW.read("/home/pi/" + readfile, 2)
        start = times[0]  # 1st time in array
        data_float = numpy.array(data).astype(numpy.float)
        numpy_average = numpy.average(data_float)  # Complete avarage
        numpy_max = numpy.amax(data_float)  # max value of array
        avrgtemp = round(numpy_average, 2)
        tup_temp_refined = (start, avrgtemp)
        fileRW.write("/home/pi/" + writefile, tup_temp_refined)
        # delete file after use to give clean start for next average
        os.remove("/home/pi/" + readfile)
        name = str(readfile.split(".csv")[0]).replace("_", " ")
        logger.debug("Average temperature for %s is: %s", name, avrgtemp)
        logger.debug("Max temperature for %s is: %s", name, numpy_max)
        logger.debug("Combined data for %s is: %s", name, tup_temp_refined)
        return tup_temp_refined  # posted to http server
