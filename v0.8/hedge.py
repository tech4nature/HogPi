import output
import post
import power
import subprocess
import thermo
import weight
from time import sleep
from datetime import datetime
import glob
import os
import led

fileRW = output.Output()
web = post.http()
battery = power.Power()
thermo_sensor = thermo.sensor()
weight_sensor = weight.sensor()


while True:
    d = datetime.now()
    hrs = int(d.strftime("%H"))
    min = int(d.strftime("%M"))
    sec = int(d.strftime("%S"))
    time = sec + (min * 60) + (hrs * 3600)
    print(time)

    if time % 3600 == 300:  # Offset by 5 min
        test = subprocess.Popen(['python3', 'video.py'])  # Record Video
        test.wait()  # Wait for Video to Finish

    elif time % 600 == 0:
        weight_sensor.tare_weight(0.6)

        weight_sensor.write('weight.csv', debug=True, time=60)  # Read Weight
        thermo_sensor.write(debug=True, time=60)  # Read Temperature

        weight_sensor.avrg('weight.csv', 'avrgweight.csv', 0.95, True)  # Average Weight
        thermo_sensor.avrg('temp_in.csv', 'avrgtemp_in.csv', True)  # Average Temperature
        thermo_sensor.avrg('temp_out.csv', 'avrgtemp_out.csv', True)  # Average Temperature
        weightJSON = fileRW.format_data_weight('avrgweight.csv', 23435445, 2343432,
                                               'weight')  # Format Weight as JSON
        tempJSON = fileRW.format_data_temp(['avrgtemp_in.csv', 'avrgtemp_out.csv'], 23435445, 2343432,
                                           'temp')  # Format Temperature as JSON
        print(weightJSON, tempJSON)
        web.post("http://10.172.100.26:8192/api/weight/", weightJSON)
        web.post("http://10.172.100.26:8192/api/temp/", tempJSON)

        # * means all if need specific format then *.csv
        # list_of_files = glob.glob('/home/pi/Videos/*')
        # latest_file = max(list_of_files, key=os.path.getctime)
        # fileRW.ftp_video(latest_file, "10.172.100.26", "ftphog", "hog1")

    else:
        sleep(1)
