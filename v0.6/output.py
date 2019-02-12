from csv import writer, reader
import json


class Output:
    @staticmethod
    def write(filename, data, debug=False):
        with open(filename, 'w') as f:
            data_writer = writer(f)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

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
    def format_data(filenames, hog_id, box_id, type):
        a = []
        for filename in filenames:
            with open('/home/pi/' + filename, 'r') as f:
                data_reader = reader(f, delimiter=',')
                times = []
                data = []
                for row in data_reader:
                    times.append(row[0])
                    data.append(row[1])
                a.append(data[0])
        a = {
            "hog_id": hog_id,
            "box_id": box_id,
            str(filename[0].split('.csv')[0]): data[0],
            str(filename[1].split('.csv')[0]): data[1],
            "time_stamp": times[0]
        }
        return a
