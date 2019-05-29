#  =======================================
# Import Statements
#  =======================================

import weight
import pir
import time
import rfid
import thermo
from multiprocessing import Process
import client
import output
import glob
import os
import pysftp
import subprocess
from datetime import datetime
#  =======================================
# Object settings
#  =======================================
pir_sensor = pir.sensor(11)
rfid_sensor = rfid.sensor()
fileRW = output.Output()
#  =======================================
# Variable settings
#  =======================================
box_id = 'box-9082242689124'
#  =======================================
# Define functions
#  =======================================


def run(type):
    if type == 'weight':
        weight_sensor = weight.sensor()
        weight_sensor.write('weight.csv', debug=True, time=10)  # Read Weight
        weight_sensor.avrg('weight.csv', 'avrgweight.csv', 0.95, True)  # Average Weight

    elif type == 'temp':
        thermo_sensor = thermo.sensor()
        thermo_sensor.write(debug=True, time=10)  # Read Temperature
        thermo_sensor.avrg('temp_in.csv', 'avrgtemp_in.csv', True)  # Average Temperature
        thermo_sensor.avrg('temp_out.csv', 'avrgtemp_out.csv', True)  # Average Temperature


def post(box_id, hog_id):
    if to_post['weight'] == True:
        weight = fileRW.read('/home/pi/avrgweight.csv', 2)
        times = fileRW.read('/home/pi/avrgweight.csv', 1)
        for i in range(len(weight)):
            time = datetime.strptime(times[i], "%Y %m %d %H %M %S")
            if weight[i] == '0.00':
                pass
            else:
                client.create_weight(box_id, 'hog-' + hog_id, weight[i], time)

    if to_post['temp'] == True:
        temps_in = fileRW.read('/home/pi/avrgtemp_in.csv', 1)
        temps_out = fileRW.read('/home/pi/avrgtemp_out.csv', 1)
        times_in = fileRW.read('/home/pi/avrgtemp_in.csv', 0)
        times_out = fileRW.read('/home/pi/avrgtemp_out.csv', 0)
        for i in range(len(temps_in)):
            time_in = datetime.strptime(times_in[i], "%Y %m %d %H %M %S")
            client.create_inside_temp(box_id, temps_in[i], time_in)
        for i in range(len(temps_out)):
            time_out = datetime.strptime(times_out[i], "%Y %m %d %H %M %S")
            client.create_outside_temp(box_id, temps_out[i], time_out)

    if to_post['video'] == True:
        os.chdir('/home/pi/Videos')
        files = [glob.glob(e) for e in ['*.mp4']]
        for file in files[0]:
            strtime = file.split('_')[0]
            time = datetime.strptime(strtime, '%Y-%m-%d-%H-%M-%S')
            client.upload_video(box_id, 'hog-' + hog_id, '/home/pi/Videos/' + file, time)
            os.remove('/home/pi/Videos/' + file)


def cleanup():
    os.chdir('/home/pi/')
    files_grabbed = [glob.glob(e) for e in ['*.csv']]
    for file in files_grabbed[0]:
        fileRW.clear_data('/home/pi/' + file)


#  =======================================
# Main Loop
#  =======================================
while True:
    start_time = time.time()
    to_post = {'weight': True, 'temp': True, 'video': True}  # Used for partial posts
    if pir_sensor.read() == 0:
        print('Started')
        rfid_tag = rfid_sensor.read()[-16:]
        #  =======================================
        # Weight, Temp and Video
        #  =======================================
        for i in to_post:
            try:
                if i != 'video':  # Video had to be run outside of Process
                    process = Process(target=run(i))
                    # We start the process and we block for 120 seconds.
                    process.start()
                    process.join(timeout=120)
                    # We terminate the process.
                    process.terminate()
                else:  # Runs video
                    print('Running Video')
                    try:
                        subprocess.check_output(
                            ['python3', '/home/pi/v0.8.3/video.py'], timeout=120)
                    except subprocess.CalledProcessError as e:
                        print('An error has occured, ' + i + ' will not be posted')
                        to_post['video'] = False

            except Exception as e:
                print('An error has occured, ' + i + ' will not be posted')
                to_post[i] = False

        post(box_id, rfid_tag)  # Posts data
        print('Post Completed')
        cleanup()
        #  =======================================
        # 10 Minute Check
        #  =======================================
        end_time = time.time()
        time_taken = end_time - start_time
        if time_taken < 600:
            time.sleep(600 - time_taken)

    elif start_time % 3600 <= 60:
        remoteCam = pysftp.Connection('raspberrypi.local', username='pi', password='hog1hog1')
        remoteCam.cd('/home/pi/Videos')
        files = remoteCam.list_dir()

        for file in files:
            if '.mp4' in file:
                remoteCam.get(file, '/home/pi/Videos')
                remoteCam.remove(file)
