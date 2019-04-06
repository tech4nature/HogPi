from ftplib import FTP

# domain name or server ip:
ftp = FTP('127.0.0.1')
ftp.login(user='ftp_test', passwd='hog1')

ftp.cwd('/')


def placeFile():

    filename = '/home/jack/Videos/Stuff/Applied Deep Learning with PyTorch - Full Course-CNuI8OWsppg.mp3'
    fname = 'Applied Deep Learning with PyTorch - Full Course-CNuI8OWsppg.mp3'
    ftp.storbinary('STOR ' + '/' + fname, open(filename, 'rb'))
    ftp.quit()


placeFile()
