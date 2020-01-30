import subprocess


def pull_videos(ip):
    subprocess.run(['rsync', f'pi@{ip}:/home/pi/Videos/*', '--remove-source-files', '-avz', './Videos/'])
