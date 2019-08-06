from hx711 import HX711
from time import sleep, strftime
from datetime import datetime, timedelta
from output import Output
import numpy
import os
import logging

fileRW = Output()


logger = logging.getLogger(__name__)


class sensor:
    def __init__(self):
        # Sets up scales
        global hx
        self.No_Tare = False
        hx = HX711(5, 6)
        hx.set_reading_format("LSB", "MSB")
        hx.set_reference_unit(451)  # calibrated on 1000g
        hx.reset()
        hx.tare()

        check = os.path.isfile("/home/pi/weight.csv")  # checks if file exists
        if check == False:
            open("/home/pi/weight.csv", "x")  # if not creates file
        check = os.path.isfile("/home/pi/tare_weight.csv")  # checks if file exists
        if check == False:
            open("/home/pi/tare_weight.csv", "x")  # if not creates file

    def tare_weight(self, decimal_of_max):
        # checks if weight.csv exists and is non-empty
        if (
            os.path.isfile("/home/pi/weight.csv")
            and os.path.getsize("/home/pi/weight.csv") > 0
        ):
            data = fileRW.read("/home/pi/weight.csv", 1)
            a = numpy.array(data).astype(numpy.float)
            logger.debug("this is last value to use as a[-1] %s", a[-1])
            # test if the last value is below 90% retare weight
            if a[-1] > decimal_of_max * numpy.amax(a) and a[-1] > 100:
                # set flag to allow no tare
                self.No_Tare = True
                logger.debug("Set this if you do not want a tare")
        else:
            # set flag to allow tare
            self.No_Tare = False
            # Set this if you WANT a tare
        return

    def get_time(self):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        logger.debug("Raw time: %s", d)
        logger.debug("Refined time: %s", x)
        return x

    def read(self):
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
        logger.debug("Data: %s", val)
        logger.debug("Combined: %s", tup_weight)
        sleep(0.5)
        return tup_weight

    def write(self, filename, iterations=10):
        i = 0
        while i <= iterations:
            data = self.read()
            logger.debug("Data to write: %s", data)
            fileRW.write("/home/pi/" + filename, data)  # append
            i += 1
            logger.debug("this is the iteration: %s", i)

    def avrg(self, readfile, writefile):
        # declarations
        sum_count = 0  # declare before sum_count
        valid_number = 0  # decalare before use to avoid negative division
        count = True
        starttime = ""  # declare before use to avoid undeclared error
        times = fileRW.read("/home/pi/" + readfile, 0)
        data = fileRW.read("/home/pi/" + readfile, 1)
        start = times[0]  # set to 1st time incase no weight readings
        data_array = numpy.array(data).astype(numpy.float)
        # find the mean
        numpy_average = numpy.median(data_array)  # Complete avarage
        Q1 = numpy.percentile(data_array, 25, interpolation='midpoint') # quarter at 25%
        Q3 = numpy.percentile(data_array, 75, interpolation='midpoint')
        logger.debug("Median is... %s", numpy_average)
        logger.debug("Q1 value is .... %s", Q1)
        logger.debug("Q3 value is .... %s", Q3)
        j = 0
        for i in numpy.nditer(data_array):  # why data array when data is list ??
            if i > Q1 and i < Q3 :  # Only use values in IQR
                sum_count = sum_count + i  # count the sum
                valid_number = valid_number + 1  # count the number
                if count == True:  # need to get index of i then lookup timestamp
                    start = times[j]
                    count = False
                logger.debug(i)
            else:
                logger.debug("Do not use")
            j += 1
        if valid_number == 0:
            # check for zero division
            valid_number = 1
            starttime = datetime.strptime(
                start, "%Y %m %d %H %M %S"
            )  # 1st item in list times
        # calculate averages
        sp_average = sum_count / valid_number  # gives average weight of hedgehog
        tup_weight_refined = ("Average Weight", start, "%.2f" % sp_average)
        fileRW.write("/home/pi/" + writefile, tup_weight_refined, True)
        # delete file after use to give clean start for next average
        os.remove("/home/pi/" + readfile)
        logger.debug(sum_count)
        logger.debug(valid_number)
        logger.debug("The real average is: %s", sp_average)
        logger.debug("Start time is: %s", starttime)
        logger.debug("The combined data is: %s", tup_weight_refined)
        return tup_weight_refined  # http post this value
