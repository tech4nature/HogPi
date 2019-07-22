from ftplib import FTP
import glob
import os
from datetime import datetime
from time import sleep
import logging

logger = logging.getLogger(__name__)


def post_logs(username, base_filename, directory, box_id):
    ftp = FTP('91.208.99.4')
    ftp.login(username, open('/home/pi/ftp_password.txt', 'r').read()[:11])
    os.chdir(directory)
    files = [glob.glob(e) for e in [base_filename + ".log*"]][0]
    for file in files:
        filename = box_id + '-' + datetime.now().strftime('%Y %m %d %H %M %S').replace(' ', '-') + '.log'
        ftp.storbinary('STOR ' + filename, open(file, 'rb'))
        sleep(1)  # So generated filenames are always different
        logger.info('Posted')
