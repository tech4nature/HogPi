from ftplib import FTP
import datetime
import os
SOURCE_DIR = '/home/pi/HogPi/'
box_id = 'box-7373203790301'

def send_data(self, data_name, ftp_user, ftp_password, ftp_directory, box_id, hog_id=1234):

    send_time = datetime.datetime.now().strftime('%d-%m-%YT%H:%M:%S')
    filename = data_name + '_' + send_time + '_' + str(box_id) + '_' + str(hog_id) + '.csv'
    ftp = FTP('91.208.99.4')
    ftp.login(ftp_user, ftp_password)
    print(filename)
    print(ftp.getwelcome())  # checks ftp connection
    # ftp.cwd(ftp_directory)
    filesource = SOURCE_DIR + data_name + '.csv'
    print(filesource)
    # Myfile = open(filesource, rb)  # open in binary
    with open(filesource, 'rb') as myfile:
        ftp.storbinary('STOR ' + filename, myfile)
        print('all done quitting')
        ftp.quit()
    os.chdir(SOURCE_DIR)
    # os.remove(data_name + '.csv')
    return filename

if __name__ == "__main__":
    send_data('e_log', 'ftpk@robotacademy.co.uk','Angelgabe23', '/', box_id=1001, hog_id=rfid_tag)
