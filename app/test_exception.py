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
new_save_data = save_data_txt.data('/home/pi/all_data.csv')
error_log = save_data_txt.data('/home/pi/full_log.csv')
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
# Commissioning file confirmation
#  =======================================
filename = new_data_ftp.send('start_log', 'ftpk@robotacademy.co.uk',
                             'Angelgabe23', '/', box_id=1001, hog_id=rfid_tag)
print('the start ftp complete entering main program' + filename)
# Main loop
#  =======================================
#rfid read failure
a = "RFID read failure"
print('a')
error_log.write(a,'/home/pi/full_log.csv')
filename = new_data_ftp.send('full_log', 'ftpk@robotacademy.co.uk',
                             'Angelgabe23', '/', box_id=1001, hog_id=rfid_tag)
