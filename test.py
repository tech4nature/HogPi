import requests
from datetime import datetime

weightDict = {
    "hog_id": 23435445,  # not sure about format yet
    "box_id": 2343432,
    "weight": 23,
    "time_stamp": "2019 12 31 23 59 59",
}

tempDict = {
    "hog_id": 23435445,  # not sure about format yet
    "box_id": 2343432,
    "temp": 23,
    "time_stamp": "2019 12 31 23 59 59",
}

r = requests.post('http://10.172.100.26:8192/api/weight/', json=weightDict)
r = requests.post('http://10.172.100.26:8192/api/temp/', json=tempDict)
