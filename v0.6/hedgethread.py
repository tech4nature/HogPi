import output
import post
import power
import subprocess
import thermo
import weight
import threading

fileRW = output.Output()
web = post.http()
battery = power.Power()
thermo_sensor = thermo.sensor()
weight_sensor = weight.sensor()

threading.Thread(target=weight_sensor.tare_weight(0.6))

threading.Thread(target=weight_sensor.write('weight.csv', True))  # Read Weight
threading.Thread(target=thermo_sensor.write('temp.csv', True))  # Read Temperature
# test = subprocess.Popen(['python3', 'video.py'])  # Record Video
# test.wait()  # Wait for Video to Finish
threading.Thread(target=thermo_sensor.avrg('temp.csv', 'avrgtemp.csv', True))  # Average Temperature
weightJSON = fileRW.format_data('avrgweight.csv', 23435445, 2343432,
                                'weight')  # Format Weight as JSON
tempJSON = fileRW.format_data('avrgtemp.csv', 23435445, 2343432,
                              'temp')  # Format Temperature as JSON
web.post("https://ptsv2.com/t/jfvar-1548499236/post", weightJSON)
web.post("https://ptsv2.com/t/jfvar-1548499236/post", tempJSON)
