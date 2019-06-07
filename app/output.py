from csv import writer, reader
import json
from ftplib import FTP
import os


class Output:
    @staticmethod
    def write(filename, data, debug=False):
        with open(filename, 'a') as f:
            data_writer = writer(f)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

    @staticmethod
    def clear_data(path):
        os.remove(path)
        open(path, 'w+')

    @staticmethod
    def read(filename, column, debug=False):
        with open(filename, 'r') as f:
            data_reader = reader(f, delimiter=',')
            data = []
            for row in data_reader:
                data.append(row[column])
            return data

    @staticmethod
    def setup_hogbox(name, owner, address1, address2, postcode, status, email, maint, phone, occupants, setupdate, field1, field2, x, y):
        # XXX unused?
        a = {"name": name,
             "owner": owner,
             "address1": address1,
             "address2": address2,
             "postcode": postcode,
             "status": status,
             "type": 'res',
             "emailadd": email,
             "maint": maint,
             "phone": phone,
             "occupants": occupants,
             "setupdate": setupdate,
             "field1": field1,
             "field2": field2,
             "circle": {
                 "coordinates": [x, y]
             }
             }
        return a

    @staticmethod
    def format_data_weight(filename, hog_id, box_id, type):
        # XXX unused?
        with open('/home/pi/' + filename, 'r') as f:
            data_reader = reader(f, delimiter=',')
            times = []
            data = []
            for row in data_reader:
                times.append(row[0])
                data.append(row[1])
        a = {
            "hog_id": hog_id,
            "box_id": box_id,
            "weight": data[-1],
            "time_stamp": times[0]
        }
        return a

    @staticmethod
    def format_data_temp(filenames, hog_id, box_id, type):
        # XXX unused?
        data_both = []
        for filename in filenames:
            with open('/home/pi/' + filename, 'r') as f:
                data_reader = reader(f, delimiter=',')
                times = []
                data = []
                for row in data_reader:
                    times.append(row[0])
                    data.append(row[1])
                data_both.append(data[0])
        b = {
            "hog_id": hog_id,
            "box_id": box_id,
            str(filenames[0].split('.csv')[0]): data_both[0],
            str(filenames[1].split('.csv')[0]): data_both[1],
            "time_stamp": times[0]
        }
        return b

    @staticmethod
    def ftp_video(filename, server, username, password):
        # XXX unused?
        ftp = FTP(server)
        ftp.login(user=username, passwd=password)

        filename = filename
        fname = str(filename.split('/')[-1])
        ftp.storbinary('STOR ' + '/' + fname, open(filename, 'rb'))
        ftp.quit()
