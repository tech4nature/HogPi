import json
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


class clientPost:
    def __init__(self, host, username, password):
        global HOGHOST
        global AUTH
        HOGHOST = 'http://connectionengine.co.uk/'
        AUTH = HTTPBasicAuth(username, password)

    def create_location(self, code, name):
        data = {
            "code": code,
            "name": name
        }

        return requests.post(
            HOGHOST + '/api/locations/', data=data, auth=AUTH).json()

    def _create_measurement(self, location_id, measurement_type,
                            measurement=None, hog_id=None):
        data = {
            "hog_id": hog_id,
            "measurement_type": measurement_type,
            "observed_at": datetime.utcnow().isoformat(),
            "location_id": location_id
        }
        if measurement is not None:
            data["measurement"] = measurement

        return requests.post(
            HOGHOST + '/api/measurements/', data=data, auth=AUTH).json()

    def create_weight(self, location_id, hog_id, weight):
        return _create_measurement(location_id, "weight", weight, hog_id)

    def create_inside_temp(self, location_id, temp):
        return _create_measurement(location_id, "in_temp", temp)

    def create_outside_temp(self, location_id, temp):
        return _create_measurement(location_id, "out_temp", temp)

    def upload_video(self, location_id, hog_id, video_path):
        measurement = _create_measurement(location_id, "video", hog_id=hog_id)
        print(measurement)
        measurement_id = measurement['id']
        files = {'video': open(video_path, 'rb')}
        url = HOGHOST + '/api/measurements/{}/video/'.format(measurement_id)
        return requests.put(url, files=files, auth=AUTH).json()

    def get_data(self, place):
        return json.dumps(
            requests.get(
                HOGHOST + '/api/measurements/?location=myplace').json(),
            indent=2)
