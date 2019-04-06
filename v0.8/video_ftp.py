from ftplib import FTP
import datetime
import os


class ftp:

    def __init__(self):
        global SOURCE_DIR
        SOURCE_DIR = '/home/pi/Videos/'
        # Sets up ftp

    def send_video(self, video_name, ftp_user, ftp_password, ftp_directory, box_id=1001, hog_id=1234):

        send_time = datetime.datetime.now().strftime('%d-%m-%YT%H:%M:%S')
        filename = video_name + '_' + send_time + '_' + str(box_id) + '_' + str(hog_id) + '.mp4'
        ftp = FTP('91.208.99.4')
        ftp.login(ftp_user, ftp_password)
        print(filename)
        print(ftp.getwelcome())  # checks ftp connection
        # ftp.cwd(ftp_directory)
        filesource = SOURCE_DIR + video_name + '.mp4'
        print(filesource)
        # Myfile = open(filesource, rb)  # open in binary
        with open(filesource, 'rb') as myfile:
            ftp.storbinary('STOR ' + filename, myfile)
            print('all done quitting')
            ftp.quit()
        os.chdir('/home/pi/Videos')
        os.remove(video_name + '.mp4')

        return filename
