import subprocess
from datetime import datetime
from time import strftime
import os
import sys

of = '/home/pi/Videos/'  # output folder
of1 = of + '1stPASS.mp4'
rectime = '10'  # record time of 10s

# ffmpeg 1st Pass record
arec = subprocess.Popen(['arecord', '-D', 'mic_mono', '-c1', '-r', '48000', '-f',
                         'S32_LE', '-t', 'wav', '-V', 'mono', '-v', '-'], stdout=subprocess.PIPE)
ffmpeg1 = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-r', '25', '-video_size', '1280x720', '-pixel_format', 'yuv422p', '-input_format', 'h264',
                            '-i', '/dev/video0', '-i', '-', '-c:a', 'mp3', '-c:v', 'copy', '-r', '25', '-timestamp', 'now', '-t', rectime, '-y', of1], stdin=arec.stdout)
# arec.stdout.close()  # pipe is already attached to ffmpeg1, and unneeded in this process
ffmpeg1.wait()
arec.terminate()
