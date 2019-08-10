from ftplib import FTP


def ftp_post(filename, file, username, password, ip):
    ftp = FTP(ip)
    ftp.login(user=username, passwd=password)
    ftp.storbinary('STOR ' + filename, open(file, 'rb'))
