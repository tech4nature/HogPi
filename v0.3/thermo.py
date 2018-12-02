from datetime import datetime, timedelta
from csv import writer, reader
from time import sleep, strftime


class sensor:
    def __init__(self):
        # Sets up thermostat
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        global base_dir
        global device_folder
        global device_file

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'

    def get_time(self, debug):
        d = datetime.now()
        x = d.strftime("%Y %m %d %H %M %S")
        if debug == True:
            print("Raw time: ", d)
            print("Refined time: ", x)
        return x

    def read_temp_raw(self):
        # Gets raw data off the thermostat
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read(self, debug):
        # Refines the raw data to something readable
        lines = sensor.read_temp_raw(self)
        t = sensor.get_time(False)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            tup_temp = (t, temp_c)
            if debug == True:
                print("Raw data: ", lines)
                print("Time: ", t)
                print("Data and time: ", tup_temp)
            return tup_temp

    def write(self, filename, debug):
        with open(os.path.dirname(os.path.realpath(__file__)) + filename, 'w+', newline='') as f:
            data = sensor.read(False)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

    def avrg(self, readfile, writefile, debug):
        with open(os.path.dirname(os.path.realpath(__file__)) + readfile, 'r') as f:
            data = [row[1] for row in reader(f, delimiter=';')]
            times = [row[0] for row in reader(f, delimiter=';')]
            data_float = np.array(data).astype(np.float)
            np_average = np.average(data_float)  # Complete avarage
            np_max = np.amax(data_float)  # max value of array
            starttime = datetime.strptime(times[0], '%Y %m %d %H %M %S')  # 1st item in list times
            tup_temp_refined = (starttime, np_average)
            if debug == True:
                print("Average temperature is: ", np_average)
                print("Max temperature is: ", np_max)
                print("Start time is: ", starttime)
                print("Conbined data: ", tup_temp_refined)
            return tup_temp_refined  # posted to http server
