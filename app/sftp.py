import pysftp


def pull_videos(ip, username, password):
    remoteCam = pysftp.Connection(ip, username=username, password=password)
    remoteCam.cd('/home/pi/Videos')
    files = remoteCam.list_dir()
    for file in files:
        if 'mp4' in file:
            remoteCam.get(file, '/home/pi/Videos')
            remoteCam.remove(file)
