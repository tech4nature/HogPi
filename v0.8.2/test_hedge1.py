#  =======================================
# Object settings
#  =======================================
import subprocess
import thermo
import weight
import pir
import time
import rfid
import data_ftp
import client
#  =======================================
# Object settings
#  =======================================
new_pir = pir.sensor()
new_rfid = rfid.sensor()
weight_sensor = weight.sensor()
temperature = thermo.sensor()
#  =======================================
# Variable settings
#  =======================================
# PIR variables
time_start = 0  # pir time monitor
pin_status = 0  # latch for pir
# time settings
measuring_time = 300  # sample time frame in secs
pir_time = 90  # time in secs to get chip reading
weight_time = 10  # time in secs to get weight of animal
time_length = 0  # length from time start value set 0 intitally
video_time = 10  # time in secs for video length
temp_time = 10  # time in secs for temp measure
# rfid read
rfid_tag = 'TagNotPresent'  # basic starting value
rfid_timedout = 0
# weight system settings

# video settings

# temp settings

# post settings

location = 'box-9082242689123'

# Next Sensor
#  =======================================
# Pin declarations
#  =======================================
pir_pin = 11  # pir pin
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
        try:
            # print(rfid_tag)
            rfid_tag = new_rfid.read()
            # print(rfid_tag)
            # print(time_length)no I have not started
            time.sleep(0.1)
            if (time_length + 0.1) > pir_time:
                rfid_timedout = 1  # set the timeout on the rfid
                # print('exit rfid')
        except Exception as e:
            # rfid read failure
            a = "RFID read failure" + getattr(e, 'message', repr(e))
            print('a')
            continue

#  ********** Read weight  ************
# elif pin_status == 1 and (len(rfid_tag) > 15 or rfid_timedout == 1):

    elif pin_status == 1 and (rfid_timedout == 1 or len(rfid_tag) > 15):
        try:
            weight_sensor.tare_weight(0.6)
            weight_sensor.read(True)
            weight_sensor.write('weight.csv', weight_time, True)
            avg_weight = weight_sensor.avrg('weight.csv', 'avrweight.csv', -1, True)
        except Exception as e:
            a = "weight read failure" + getattr(e, 'message', repr(e))
            print('a')
            continue

        #  ********** Read temp ************
        try:
            temperature.write(time=temp_time, debug=True)
            avg_tempin = temperature.avrg('temp_in.csv', 'avrtempin.csv', debug=True)
            avg_tempout = temperature.avrg('temp_out.csv', 'avrtempout.csv', debug=True)
            time.sleep(1)  # wait to allow resources to be released

        except Exception as e:
            a = "temp read failure" + getattr(e, 'message', repr(e))
            print('a')
            continue
        #  ********** Record video & post ************
        # Record video
        try:
            test = subprocess.Popen(['python3', '/home/pi/v0.8/video.py'])
            test.wait()
            test.terminate()
        except Exception as e:
            a = "Video failure" + getattr(e, 'message', repr(e))
            print('a')
            continue

        try:
            #  ********** Post Data**************
            client.create_weight(location, 'hog-' + rfid_tag, avg_weight)
            client.create_inside_temp(location, avg_tempin)
            client.create_outside_temp(location,  avg_tempout)
            # client.upload_video(location, 'hog-' + rfid_tag, '/home/pi/Videos/hog_video.mp4')

            #  ********** reintialise variables*************
            rfid_tag = 'TagNotPresent'
            rfid_timedout = 0

        except Exception as e:
            a = "ftp failure" + getattr(e, 'message', repr(e))
            print('a')
            continue

        #  ********** reset data ***********
    elif time_length > measuring_time:
        # print('Looking for PIR reading')
        pin_status = 0  # reset status and continue until state is read again
