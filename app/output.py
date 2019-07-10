from csv import writer, reader
import json
from ftplib import FTP
import os


class Output:
    @staticmethod
    def write(filename, data, debug=False):
        with open(filename, "a") as f:
            data_writer = writer(f)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

    @staticmethod
    def clear_data(path):
        os.remove(path)
        open(path, "w+")

    @staticmethod
    def read(filename, column, debug=False):
        with open(filename, "r") as f:
            data_reader = reader(f, delimiter=",")
            data = []
            for row in data_reader:
                data.append(row[column])
            return data
