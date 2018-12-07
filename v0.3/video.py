import subprocess
from datetime import datetime
from time import strftime
import os

class ffmpeg:
    def __init__(self):
        of = os.path.dirname(os.path.realpath(__file__))
    def record(self, filename, rectime, debug):
        # ffmpeg 1st Pass record
        global of1
        of1 = of + filename
        arec = subprocess.Popen(['arecord', '-D', 'mic_mono', '-c1', '-r', '48000', '-f',
                         'S32_LE', '-t', 'wav', '-V', 'mono', '-v', 'audio'], stdout=subprocess.PIPE)
        ffmpeg1 = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-r', '25', '-video_size', '1280x720', '-pixel_format', 'yuv422p', '-input_format',
                            'h264', '-i', '/dev/video0', '-i', 'audio', '-c:a', 'mp3', '-c:v', 'copy', '-r', '25', '-timestamp', 'now', '-t', rectime, '-y', of1], stdin=arec.stdout)
        arec.stdout.close()  # pipe is already attached to ffmpeg1, and unneeded in this process
        ffmpeg1.wait()
        arec.terminate()

    def extract_time(self, debug):
        # ffprobe to extract recording time and date and turn into offset seconds
        command = ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=creation_time', '-of',
           'default=nw=1:nk=1', '-i', of1]
        output = subprocess.check_output(command).decode('utf-8')

        d = output[:-9]
        d = d.replace('-', ' ').replace('T', ' ').replace(':', ' ')
        filename = d.replace(' ', '-')
        starttime = datetime.strptime(d, '%Y %m %d %H %M %S')
        offset = starttime.timestamp()
        if debug == True:
            print(output)
            print(d)
            print(starttime)
            print(offset)

    def sync_av(self, filename, debug):
        # ffmpeg 2nd pass to sync audio and video
        global of2
        of2 = of + filename
        ffmpeg2 = subprocess.Popen(['ffmpeg', '-i', of1, '-itsoffset', '00:00:00.5',
                            '-i', of1, '-c:v', 'copy', '-c:a', 'copy', '-map', '0:1', '-map', '1:0', '-y', of2])
        ffmpeg2.wait()

    def BITC_flip(self, filename, debug):
        # ffmpeg 3rd pass to add BITC and flip video !
        of3 = of + filename
        filter = 'vflip, drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSans.ttf:fontsize=48:text=\'%{pts\:localtime\:' + \
        str(offset) + '\\:%Y %m %d %H %M %S}\': fontcolor=white@1: x=10: y=10'
        if debug == True:
            print(filter)
        ffmpeg3 = subprocess.Popen(['ffmpeg', '-i', of2, '-vf', filter, '-c:v',
                            'libx264', '-preset', 'ultrafast', '-c:a', 'copy', '-r', '25', '-y', of3])
        ffmpeg3.wait()

        # remove 1stPASS.mp4 and 2ndPASS.mp4 if ffmpeg3 is sucessful
        if ffmpeg3.returncode == 0:
            os.remove(of1)
            os.remove(of2)
