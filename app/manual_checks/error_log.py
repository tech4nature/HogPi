import os
import json


class data:

    def __init__(self,path):

        check = os.path.isfile(path)  # checks if file exists
        if check is False:
            open(path, 'x')  # if not creates file

    def write(self, dict, path):
        json.dump(dict, open(path, "a", newline="\n"))
        print('all done')
