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
#  =======================================
# Object settings
#  =======================================
new_pir = pir.sensor()
new_rfid = rfid.sensor()
weight_sensor = weight.sensor()
temperature = thermo.sensor()
new_ftp = video_ftp.ftp()
#  =======================================
# Variable settings
#  =======================================
# PIR variables
time_start = 0  # pir time monitor
pin_status = 0  # latch for pir
# time settings
measuring_time = 300  # sample time 600 s
pir_time = 60  # time in secs to get chip reading
weight_time = 60  # time in secs to get weight of animal
time_length = 0  # length from time start value
video_time = 20  # time in secs for video length
temp_time = 20  # time in secs for temp measure
# rfid read
rfid_read = 0  # flag to say operation is complete
# weight system settings
weight_read = 0  # flag to say operation is complete
# video settings
video_rec = 0  # flag to say video has been recorded

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
    time_length = time.time() - time_start  # calculate the length of time
    GPIO = new_pir.read(pir_pin)
    if GPIO and pin_status == 0:
        print('Main running')
        pin_status = 1  # set pin status
        time_start = time.time()  # set time start

#  ********** Read RFID for 60Sec ************
    elif time_length < pir_time and pin_status == 1:  # pir on and first 60s
        a = new_rfid.read()
        print(a)
        print(time_length)
        time.sleep(0.1)
        rfid_read = 1
#  ********** Read weight for 60Sec ************
    elif (rfid_read == 1 and pin_status == 1):
        weight_sensor.tare_weight(0.6)
        weight_sensor.read(True)
        weight_sensor.write('weight.csv', 10, True)
        weight_sensor.avrg('weight.csv', 'avrweight.csv', 0.95, True)
        rfid_read = 0
        weight_read = 1
#  ********** Read temp for 30Sec ************
    elif (weight_read == 1 and pin_status == 1):
        temperature.write(time=temp_time, debug=True)
        temperature.avrg('temp_in.csv', 'avrtempin.csv', debug=True)
        temperature.avrg('temp_out.csv', 'avrtempout.csv', debug=True)
        weight_read = 0
        video_rec = 1
        time.sleep(10)  # wait to allow resources to be released
#  ********** Record video & post ************
# video time has to be adjusted in video.def foo():
    elif (video_rec == 1 and pin_status == 1):
        # Record video
        test = subprocess.Popen(['python3', '/home/pi/v0.8/video.py'])
        test.wait()
        test.terminate()
        #  Post Video
        filename = new_ftp.send_video('hog_video', 'ftpk@robotacademy.co.uk',
                                      'Angelgabe23', '/', box_id=1001, hog_id=1234)
        print(filename)
        video_rec = 0
#  ********** Post Data************

#  ********** Post Data************
    elif time_length > measuring_time:
        print('Main NOT running')
        pin_status = 0  # reset status and continue until state is read again
