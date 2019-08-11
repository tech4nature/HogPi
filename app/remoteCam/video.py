import subprocess
from datetime import datetime
from time import strftime
import os
import sys
import led
import logging
import pytz
import tzlocal


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    #    irled = led.sensor(3)  # Instantiate led class and assign the pin the BCM3

    of = "/home/pi/Videos/"  # output folder
    of1 = of + "1stPASS.mp4"
    rectime = "10"  # record time of 10s

    # ffmpeg 1st Pass record
    #   irled.on()  # Turn led on

    # removed all audio from this files

    ffmpeg1 = subprocess.Popen(
        [
            "ffmpeg",
            "-f",
            "v4l2",
            "-r",
            "25",
            "-video_size",
            "1280x720",
            "-pixel_format",
            "yuv422p",
            "-input_format",
            "h264",
            "-i",
            "/dev/video0",
            "-c:v",
            "copy",
            "-r",
            "25",
            "-timestamp",
            "now",
            "-t",
            rectime,
            "-y",
            of1,
        ]
    )
    ffmpeg1.wait()
    #  irled.off()  # Turn led off

    # ffprobe to extract recording time and date and turn into offset seconds
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format_tags=creation_time",
        "-of",
        "default=nw=1:nk=1",
        "-i",
        of1,
    ]
    output = subprocess.check_output(command).decode("utf-8")
    logger.debug("Got output %s", output)

    local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
    d = output[:-9]
    d = d.replace("-", " ").replace("T", " ").replace(":", " ")

    starttime = datetime.strptime(d, "%Y %m %d %H %M %S")
    local_time = starttime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    offset = local_time.timestamp()
    logger.debug("Computed date offset %s", offset)
    d = local_time.strftime("%Y %m %d %H %M %S")
    filename = d.replace(" ", "-")

    # ffmpeg 3rd pass to add BITC and flip video !
    of3 = of + filename + "_ext.mp4"  # added _ext to demark external camera
    filter = (
        "drawtext=fontfile=/home/pi/.fonts/NovaRound.ttf:fontsize=48:text='%{pts\:localtime\:"
        + str(offset)
        + "\\:%Y %m %d %H %M %S}': fontcolor=white@1: x=10: y=10"
    )
    logger.debug("Using ffmpeg filter %s", filter)
    ffmpeg3 = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            of1,
            "-vf",
            filter,
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-b:v",
            "1600k",
            "-r",
            "25",
            "-an",
            "-y",
            of3,
        ]
    )  # tried '-c:v', 'h264_omx', '-profile', '100'
    ffmpeg3.wait()

    # remove 1stPASS.mp4 and 2ndPASS.mp4 if ffmpeg3 is sucessful
    # if ffmpeg3.returncode == 0:
    # os.remove(of1)
    # os.remove("/home/pi/jackTest/audio")

    sys.exit()
