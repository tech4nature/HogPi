#  =======================================
# Import Statements
#  =======================================
import ftp
import weight
import pir
import logging
import logging.handlers
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
import sftp
from datetime import datetime
from pathlib import Path


#  =======================================
# Object settings
#  =======================================
pir_sensor = pir.sensor(11)  # BCM
rfid_sensor = rfid.sensor()
fileRW = output.Output()
#  =======================================
# Variable settings
#  =======================================
box_id = "box-9082242689124"
cycle_time = 600
last_ran = None
PIZERO_IP = '10.170.1.'
PIZERO_IP_MIN = 11
PIZERO_IP_MAX = 20
PIZERO_FTP_USERNAME = 'pi'
PIZERO_FTP_PASSWORD = 'hog1hog1'
#  =======================================
# Define functions
#  =======================================

logger = logging.getLogger(__name__)


def read_and_average(measurement_type):
    if measurement_type == "weight":
        weight_sensor = weight.sensor()
        weight_sensor.write("weight.csv", iterations=10)  # Read Weight
        weight_sensor.avrg("weight.csv", "avrgweight.csv", 0.95)  # Average Weight

    elif measurement_type == "temp":
        thermo_sensor = thermo.sensor()
        thermo_sensor.write(iterations=10)  # Read Temperature
        thermo_sensor.avrg("temp_in.csv", "avrgtemp_in.csv")  # Average Temperature
        thermo_sensor.avrg("temp_out.csv", "avrgtemp_out.csv")  # Average Temperature


def post(box_id, hog_id, to_post):
    if to_post["weight"] == True:
        weight = fileRW.read("/home/pi/avrgweight.csv", 2)
        times = fileRW.read("/home/pi/avrgweight.csv", 1)
        posts_success = True
        for i in range(len(weight)):
            time = datetime.strptime(times[i], "%Y %m %d %H %M %S")
            if weight[i] == "0.00":
                pass
            else:
                try:
                    client.create_weight(box_id, "hog-" + hog_id, weight[i], time)
                    fileRW.clear_data("/home/pi/avrgweight.csv")
                except [requests.exceptions.HTTPError, JSONError] as e:
                    logger.exception("Problem posting weight from %s", box_id)

    if to_post["temp"] == True:
        temps_in = fileRW.read("/home/pi/avrgtemp_in.csv", 1)
        temps_out = fileRW.read("/home/pi/avrgtemp_out.csv", 1)
        times_in = fileRW.read("/home/pi/avrgtemp_in.csv", 0)
        times_out = fileRW.read("/home/pi/avrgtemp_out.csv", 0)
        posts_success = True
        try:
            for i in range(len(temps_in)):
                time_in = datetime.strptime(times_in[i], "%Y %m %d %H %M %S")
                client.create_inside_temp(box_id, temps_in[i], time_in)

            for i in range(len(temps_out)):
                time_out = datetime.strptime(times_out[i], "%Y %m %d %H %M %S")
                client.create_outside_temp(box_id, temps_out[i], time_out)
                fileRW.clear_data("/home/pi/avrgtemp_in.csv")
                fileRW.clear_data("/home/pi/avrgtemp_out.csv")

        except [requests.exceptions.HTTPError, JSONError] as e:
            logger.exception("Problem posting temp from %s", box_id)

    if to_post["video"] == True:
        os.chdir("/home/pi/Videos")
        files = [glob.glob(e) for e in ["*.mp4"]]
        for file in files[0]:
	    if file != '1stPass.mp4':
                strtime = file.split("_")[0]
                time = datetime.strptime(strtime, "%Y-%m-%d-%H-%M-%S")
                try:
                    client.upload_video(
                        box_id, "hog-" + hog_id, "/home/pi/Videos/" + file, time
                    )
                    os.remove("/home/pi/Videos/" + file)
                except [requests.exceptions.HTTPError, JSONError] as e:
                    logger.exception("Problem posting video from %s", box_id)


def cleanup():
    files_grabbed = [glob.glob(e) for e in ["/home/pi/*.csv"]]
    for file in files_grabbed[0]:
        if "avrg" in file:
            pass
        else:
            fileRW.clear_data(file)


#  =======================================
# Main Loop
#  =======================================
def main():
    logger.info("Main loop heartbeat")
    start_time = time.time()
    to_post = {"weight": True, "temp": True, "video": True}  # Used for partial posts
    if pir_sensor.read() == 0:
        logger.info("Started")
        rfid_tag = rfid_sensor.read()[-16:]
        #  =======================================
        # Weight, Temp and Video
        #  =======================================
        for i in to_post:
            try:
                if i != "video":  # Video had to be run outside of Process
                    process = Process(target=read_and_average(i))
                    # We start the process and we block for 120 seconds.
                    process.start()
                    process.join(timeout=120)
                    # We terminate the process.
                    process.terminate()
                else:  # Runs video
                    logger.info("Running Video")
                    try:
                        path = '/home/pi/HogPi/app/video.py'
                        subprocess.check_output(["python3", path], timeout=120)
                    except subprocess.CalledProcessError as e:
                        logger.exception("%s cannot be posted", i)
                        to_post["video"] = False

            except Exception as e:
                logger.exception("An error has occurred")
                to_post[i] = False

        post(box_id, rfid_tag, to_post)  # Posts data
        logger.info("Post Completed")
        cleanup()
        #  =======================================
        # 10 Minute Check
        #  =======================================
        end_time = time.time()
        time_taken = end_time - start_time
        if time_taken < cycle_time:
            time.sleep(cycle_time - time_taken)
        return None

    elif last_ran != datetime.now().strftime('%H'):
        print(str(last_ran) + '          ' + datetime.now().strftime('%H'))
        last_ran = datetime.now().strftime('%H')
        for i in range(PIZERO_IP_MIN, PIZERO_IP_MAX + 1):
            response = os.system('ping -c 1 ' + PIZERO_IP + str(i))
            if 0 == response:
                sftp.pull_videos(PIZERO_IP + str(i), PIZERO_FTP_USERNAME, PIZERO_FTP_PASSWORD)
                to_post = {'weight': False, 'temp': False, 'video': True}
                post(box_id, 'outside', to_post)
        # weight_sensor = weight.sensor() # Will be run once an hour if PIR not triggered
        # weight_sensor.tare_weight()  # Commented because awaiting function refactor
        os.chdir("/home/pi/")
        files = [glob.glob(e) for e in ["*.log"]]
        for file in files[0]:
            filename = box_id + datetime.now().strftime('Y-%m-%d-%H-%M-%S')
            ftp.ftp_post(filename, file, 'ftpk@robotacademy.co.uk', 'Angelgabe23', '91.208.99.4')
        return last_ran


if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.handlers.RotatingFileHandler(
            filename="hedge.log", maxBytes=1024 * 1024 * 10, backupCount=5)],
        level=logging.DEBUG,
    )
    while True:
        result = main(last_ran)
        if result:
            last_ran = result
