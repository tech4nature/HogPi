#  =======================================
# Object settings
#  =======================================
import post
import video
import subprocess
import thermo
import weight
import power
import output
import video_ftp
import pir
import time
import rfid
import save_data_txt
import data_ftp
#  =======================================
# Object settings
#  =======================================
new_pir = pir.sensor()
new_rfid = rfid.sensor()
weight_sensor = weight.sensor()
temperature = thermo.sensor()
new_ftp = video_ftp.ftp()
new_save_data = save_data_txt.data('./log.txt')
new_data_ftp = data_ftp.ftp()
#  =======================================
# Variable settings
#  =======================================
# PIR variables
time_start = 0  # pir time monitor
pin_status = 0  # latch for pir
# time settings
measuring_time = 300  # sample time frame in secs
pir_time = 90  # time in secs to get chip reading
weight_time = 60  # time in secs to get weight of animal
time_length = 0  # length from time start value set 0 intitally
video_time = 20  # time in secs for video length
temp_time = 60  # time in secs for temp measure
# rfid read
rfid_tag = 'TagNotPresent'  # basic starting value
rfid_timedout = 0
# weight system settings

# video settings

# temp settings

# Next Sensor
#  =======================================
# Pin declarations
#  =======================================
pir_pin = 11  # pir pin
#  =======================================
# Main loop
#  =======================================
while True:
    # ********** Read PIR ************
    time_length = time.time() - time_start  # calculate the length of time
    GPIO = new_pir.read(pir_pin)  # reads pir
    if GPIO and pin_status == 0:
        print('Main running')
        pin_status = 1  # set pin status
        time_start = time.time()  # set time start
        a = new_rfid.read()  # flush buffer on second loop
        a = new_rfid.read()  # flush buffer on second loop

        #  ********** Read RFID ************
    # elif (time_length < pir_time and len(rfid_tag) < 15
    #        and pin_status == 1):
    elif (time_length < pir_time and pin_status == 1 and len(rfid_tag) < 15):
        #  either the timer is on or the RFID is not detected
        print(rfid_tag)
        rfid_tag = new_rfid.read()
        print(rfid_tag)
        # print(time_length)
        time.sleep(0.1)
        if (time_length + 0.1) > pir_time:
            rfid_timedout = 1  # set the timeout on the rfid
            # print('exit rfid')
        #  ********** Read weight  ************
# elif pin_status == 1 and (len(rfid_tag) > 15 or rfid_timedout == 1):
    elif pin_status == 1 and (rfid_timedout == 1 or len(rfid_tag) > 15):
        weight_sensor.tare_weight(0.6)
        weight_sensor.read(True)
        weight_sensor.write('weight.csv', weight_time, True)
        avg_weight = weight_sensor.avrg('weight.csv', 'avrweight.csv', 0.95, True)
        #  ********** Read temp ************
        temperature.write(time=temp_time, debug=True)
        avg_tempin = temperature.avrg('temp_in.csv', 'avrtempin.csv', debug=True)
        avg_tempout = temperature.avrg('temp_out.csv', 'avrtempout.csv', debug=True)
        time.sleep(1)  # wait to allow resources to be released
        #  ********** Record video & post ************
        # Record video
        test = subprocess.Popen(['python3', '/home/pi/v0.8/video.py'])
        test.wait()
        test.terminate()
        #  Post Video
        filename = new_ftp.send_video('hog_video', 'ftpk@robotacademy.co.uk',
                                      'Angelgabe23', '/', box_id=1001, hog_id=1234)
        print(filename)
        #  ********** Post Data**************
        #  write all data into txt file
        dict_hog = {"hog_ID": rfid_tag, "location": "Brockworth"}
        new_save_data.write(dict_hog)
        new_save_data.write(avg_weight)
        new_save_data.write(avg_tempin)
        new_save_data.write(avg_tempout)
        #  ftp the file

        #  ********** reintialise variables*************
        rfid_tag = 'TagNotPresent'
        rfid_timedout = 0
        #  ********** sample pause***********
        filename = new_data_ftp.send('all_data', 'ftpk@robotacademy.co.uk',
                                     'Angelgabe23', '/', box_id=1001, hog_id=rfid_tag)
        print(filename)
        #  ********** reset data ***********
    elif time_length > measuring_time:
        print('Looking for PIR reading')
        pin_status = 0  # reset status and continue until state is read again
