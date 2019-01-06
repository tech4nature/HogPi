from csv import writer, reader

class Output:
    @staticmethod
    def write(filename, data, debug):
        with open(filename, 'w') as f:
            data_writer = writer(f)
            if debug == True:
                print("Data to write: ", data)
            data_writer.writerow(data)

    @staticmethod
    def read(filename, column, debug):
        with open('/home/pi/' + filename, 'r') as f:
            data_reader = reader(f, delimiter=',')
            data = []
            for row in data_reader:
                data.append(row[column])
            return data
