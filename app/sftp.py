import pysftp
import os


def pull_videos(ip, username, password):
    os.chdir("/home/pi/Videos")  # Set pi 3 cwd to Videos
    remoteCam = pysftp.Connection(ip, username=username, password=password)
    remoteCam.chdir("/home/pi/Videos")  # Set pi 0 cwd to Videos
    files = remoteCam.listdir()
    for file in files:
        if (
            ".mp4" in file and not "1stPASS" in file
        ):  # 1stPASS is a intermidiate file that isn't ready for posting
            remoteCam.get(file)
            remoteCam.remove(file)
