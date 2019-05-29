import output
import post
import power
import subprocess
import thermo
import weight
from time import sleep
from datetime import datetime

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

    if time % 60 == 0:
        weight_sensor.tare_weight(0.6)

        weight_sensor.write('weight.csv', debug=True)  # Read Weight
        thermo_sensor.write(debug=True)  # Read Temperature
        test = subprocess.Popen(['python3', 'video.py', '--time', '60'])  # Record Video
        test.wait()  # Wait for Video to Finish
        weight_sensor.avrg('weight.csv', 'avrgweight.csv', 0.95, True)  # Average Weight
        thermo_sensor.avrg('temp_in.csv', 'avrgtemp.csv', True)  # Average Temperature
        thermo_sensor.avrg('temp_out.csv', 'avrgtemp.csv', True)  # Average Temperature
        weightJSON = fileRW.format_data('avrgweight.csv', 23435445, 2343432,
                                        'weight')  # Format Weight as JSON
        tempJSON = fileRW.format_data(['temp_in.csv', 'temp_out.csv'], 23435445, 2343432,
                                      'temp')  # Format Temperature as JSON
        web.post("http://10.172.100.26:8192/api/weight/", weightJSON)
        web.post("http://10.172.100.26:8192/api/temp/", tempJSON)

    else:
        sleep(1)
