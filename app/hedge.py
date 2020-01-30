#  =======================================
# Import Statements
#  =======================================
from typing import Dict, List
import ftp
import numpy
import weight
import pir
import data
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
from datetime import timezone
from pathlib import Path
import requests.exceptions
import json
import tzlocal  # timecorrection

# ===================
# Load in Config File
# ===================
config = json.load(open("/home/pi/config.json", "r"))
# =================
# Variable settings
# =================
box_id = config["box_id"]
cycle_time = 100
rfid_record_time = 45
last_ran = None
PIZERO_IP = "10.170.1."
PIZERO_IP_MIN = 11
PIZERO_IP_MAX = 20
#  =======================================
# Object settings
#  =======================================
pir_sensor = pir.sensor(11)  # BCM
rfid_sensor = rfid.sensor(rfid_record_time)
fileRW = output.Output()
#  =======================================
# Define functions
#  =======================================

logger = logging.getLogger(__name__)

weight_sensor = weight.Sensor()  # Will be run once an hour if PIR not triggered
weight_sensor.tare_weight()  # Commented because awaiting function refactor


def read_and_average(measurement_type):
    if measurement_type == "weight":
        weight_data: data.Data = weight_sensor.read()
        weight_data: data.Data = weight_sensor.avrg(weight_data)
        print(weight_data.value)

    elif measurement_type == "temp":
        thermo_sensor = thermo.sensor()
        thermo_sensor.write(iterations=10)  # Read Temperature
        thermo_sensor.avrg("temp_in.csv", "avrgtemp_in.csv")  # Average Temperature
        thermo_sensor.avrg("temp_out.csv", "avrgtemp_out.csv")  # Average Temperature


def post(box_id, hog_id, to_post):
    print("posting")  # commissioning
    if to_post["weight"]:
        try:
            weights_json: Dict = json.load(open("/home/pi/HogPi/app/weight.json", "r"))
            weights: List = data.deserialise_many(weights_json)

            for weight in weights:
                if not numpy.isnan(weight.value[0]) or not weight.value[0] < 5:
                    client.create_weight(
                        box_id, "hog-" + hog_id, weight.value[0], weight.timestamp
                    )

            i = []
            json.dump(i, open("/home/pi/HogPi/app/weight.json", "w"))
        except Exception as e:
            print(e)

    if to_post["temp"] == True:
        print("post temp")  # commissioning
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

        except Exception as e:
            logger.exception("Problem posting temp from %s", box_id)

    if to_post["video"] == True:
        os.chdir("/home/pi/Videos")
        files = [glob.glob(e) for e in ["*.mp4"]]
        for file in files[0]:
            if file != "1stPASS.mp4":
                strtime = file.split("_")[0]
                time = datetime.strptime(strtime, "%Y-%m-%d-%H-%M-%S-%z")
                time = time.astimezone(timezone.utc)  # timezone correction

                try:
                    client.upload_video(
                        box_id, "hog-" + hog_id, "/home/pi/Videos/" + file, time
                    )
                    os.remove("/home/pi/Videos/" + file)
                except Exception as e:
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
def main(last_ran):
    # logger.debug("Main loop heartbeat") too much info
    hour = int(datetime.strftime(datetime.now(), "%H"))  # get hour now
    start_time = time.time()
    to_post = {"weight": True, "temp": True, "video": True}  # Used for partial posts
    if pir_sensor.read():  # only record when pir activated
        logger.debug("PIR READ")
        logger.debug("Started")
        rfid_tag = rfid_sensor.read()[-16:]  # record for fixed time after pir reading
        time.sleep(10)  # wait 10 s after rfid read to ensure animal present
        #  =======================================
        # Weight, Temp and Video
        #  =======================================
        for i in to_post:
            try:
                if i != "video":  # Video had to be run outside of Process
                    process = Process(target=read_and_average, args=(i,))
                    # We start the process and we block for 120 seconds.
                    print("process is: " + str(i))  # commissioning
                    process.start()
                    process.join(timeout=120)
                    # We terminate the process.
                    process.terminate()
                else:  # Runs video
                    logger.debug("Running Video")
                    try:
                        path = "/home/pi/HogPi/app/video.py"
                        subprocess.check_output(["python3", path], timeout=120)
                    except subprocess.CalledProcessError as e:
                        logger.exception("%s cannot be posted", i)
                        to_post["video"] = False

            except Exception as e:
                logger.exception("An error has occurred")
                to_post[i] = False

        post(box_id, rfid_tag, to_post)  # Posts data
        logger.debug("Post Completed")
        cleanup()
        #  =======================================
        # 10 Minute Check
        #  =======================================
        end_time = time.time()
        time_taken = end_time - start_time
        if time_taken < cycle_time:
            print("sleeping: " + str(cycle_time))  # commissioning
            print(cycle_time - time_taken)
            time.sleep(cycle_time - time_taken)
        return None

    elif last_ran != datetime.now().strftime("%H"):
        logger.info("Main loop heartbeat; last ran %s", last_ran)
        last_ran = datetime.now().strftime("%H")
        try:
            for i in range(PIZERO_IP_MIN, PIZERO_IP_MAX + 1):
                response = os.system("ping -c 1 " + PIZERO_IP + str(i))
                if 0 == response:
                    sftp.pull_videos(PIZERO_IP + str(i))
                    to_post = {"weight": False, "temp": False, "video": True}
                    post(box_id, "outside", to_post)
        except Exception as e:
            logger.exception("SFTP has failed")
        weight_sensor.tare_weight()  # Commented because awaiting function refactor
        os.chdir("/home/pi/HogPi/app")
        try:
            files = [glob.glob(e) for e in ["*.log"]]
            for file in files[0]:
                filename = box_id + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                ftp.ftp_post(
                    filename,
                    file,
                    "ftpk@robotacademy.co.uk",
                    "Angelgabe23",
                    "91.208.99.4",
                )
        except Exception as e:
            logger.exception("FTP has failed")
        return last_ran


class StackdriverFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(StackdriverFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        return json.dumps(
            {
                "severity": record.levelname,
                "message": record.getMessage(),
                "name": record.name,
                "time": datetime.utcfromtimestamp(record.created).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            }
        )


if __name__ == "__main__":
    handler = logging.handlers.RotatingFileHandler(
        filename="hedge.log", maxBytes=1024 * 1024 * 10, backupCount=5
    )
    handler.setFormatter(StackdriverFormatter())
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)
    while True:
        result = main(last_ran)
        if result:
            last_ran = result
