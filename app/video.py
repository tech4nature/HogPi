import subprocess
from datetime import datetime
from time import strftime
import os
import sys
import led


if __name__ == "__main__":
    irled = led.sensor(17)  # Instantiate led class and assign the pin the BCM17

    of = '/home/pi/Videos/'  # output folder
    of1 = of + '1stPASS.mp4'
    rectime = '10'  # record time of 10s

    # ffmpeg 1st Pass record
    irled.on()  # Turn led on

    arec = subprocess.Popen(['arecord', '-D', 'mic_mono', '-c1', '-r', '48000', '-f',
                             'S32_LE', '-t', 'wav', '-V', 'mono', '-v', 'audio'], stdout=subprocess.PIPE)
    ffmpeg1 = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-r', '25', '-video_size', '1280x720', '-pixel_format', 'yuv422p', '-input_format',
                                'h264', '-i', '/dev/video0', '-i', 'audio', '-c:a', 'mp3', '-c:v', 'copy', '-r', '25', '-timestamp', 'now', '-t', rectime, '-y', of1], stdin=arec.stdout)
    arec.stdout.close()  # pipe is already attached to ffmpeg1, and unneeded in this process
    ffmpeg1.wait()
    arec.terminate()
    irled.off()  # Turn led off

    # ffprobe to extract recording time and date and turn into offset seconds
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=creation_time', '-of',
               'default=nw=1:nk=1', '-i', of1]
    output = subprocess.check_output(command).decode('utf-8')
    print(output)

    d = output[:-9]
    print(d)
    d = d.replace('-', ' ').replace('T', ' ').replace(':', ' ')
    print(d)
    filename = d.replace(' ', '-')
    starttime = datetime.strptime(d, '%Y %m %d %H %M %S')
    print(starttime)
    offset = starttime.timestamp()
    print(offset)

    # ffmpeg 2nd pass to sync audio and video
    of2 = of + '2ndPASS.mp4'
    ffmpeg2 = subprocess.Popen(['ffmpeg', '-i', of1, '-itsoffset', '00:00:00.4',
                                '-i', of1, '-c:v', 'copy', '-c:a', 'copy', '-map', '0:1', '-map', '1:0', '-y', of2])
    ffmpeg2.wait()

    # ffmpeg 3rd pass to add BITC and flip video !
    of3 = of + filename + '_int.mp4'  # added _int to demark internal camera
    filter = 'drawtext=fontfile=/home/pi/.fonts/NovaRound.ttf:fontsize=48:text=\'%{pts\:localtime\:' + \
        str(offset) + '\\:%Y %m %d %H %M %S}\': fontcolor=white@1: x=10: y=10'
    print(filter)
    ffmpeg3 = subprocess.Popen(['ffmpeg', '-i', of2, '-vf', filter, '-c:v', 'libx264', '-preset',
                                'ultrafast', '-c:a', 'copy', '-r', '25', '-y', of3])  # tried '-c:v', 'h264_omx', '-profile', '100'
    ffmpeg3.wait()

    # remove 1stPASS.mp4 and 2ndPASS.mp4 if ffmpeg3 is sucessful
    if ffmpeg3.returncode == 0:
        os.remove(of1)
        os.remove(of2)
        # os.remove("/home/pi/jackTest/audio")

    sys.exit()
