import os
import glob
import time
import RPi.GPIO as GPIO
import sys
from hx711 import HX711
from csv import writer
import numpy
import csv

# def tare_weight():
# Gets the new zero on the weight scale if it has finished
# -------------------------------------
# declarations
#    old_min_weight = 0
new_min_weight = 0
# numpy_size = 0
# numpy_average = 0
min_tolerance = 100  # addition items susc as food 100g
# --------------------------------
# Read the old weight data


def tare_weight(self):
    with open('tare_weight.csv', 'r') as w_csvfile:
        mylist = [row[0] for row in csv.reader(w_csvfile, delimiter=';')]
        old_min_weight = float(mylist[0])
        print(old_min_weight)
    # find the min weight of the platform
    with open('data_weight.csv', 'r') as w_csvfile:
        mylist = [row[0] for row in csv.reader(w_csvfile, delimiter=';')]
        a = numpy.array(mylist).astype(numpy.float)
        print(numpy.amin(a))
    # compare with average weight of hog last read. This should
    # if the max weight - numpy_average is close to tare weight value is read

    if numpy.amin(a) < min_tolerance and numpy.amin(a) > -min_tolerance:
        # only write if the min is in acceptable range usually +-100 of last Value
        numpy_min = numpy.amin(a)
        with open('tare_weight.csv', 'w') as f:
            # write using the csv object change from float to string
            f.write(str(numpy_min))
            print("complete writing")
    else:
     # otherwise assume hedgehog stayed in box keep lower value of tare
        print("hedgehog in box")
        numpy_min = old_min_weight
    return numpy_min
