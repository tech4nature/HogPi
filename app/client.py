import json
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


HOGHOST = "http://connectionengine.co.uk"
AUTH = HTTPBasicAuth('tech4nature', 'hoggy')


class clientPost:
    def __init__(self):
        pass

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

        return requests.post(HOGHOST + '/api/measurements/', data=data, auth=AUTH).json()
        # if r.status_code == 200:
        # return r.json()

        # else:
        # return 'An error has occured'

    def create_weight(self, location_id, hog_id, weight):
        return self._create_measurement(location_id, "weight", weight, hog_id)

    def create_inside_temp(self, location_id, temp):
        return self._create_measurement(location_id, "in_temp", temp)

    def create_outside_temp(self, location_id, temp):
        return self._create_measurement(location_id, "out_temp", temp)

    def upload_video(self, location_id, hog_id, video_path):
        measurement = self._create_measurement(location_id, "video", hog_id=hog_id)
        if measurement == 'An error has occured':
            return 'An error has occured'
        else:
            measurement_id = measurement['id']
            files = {'video': open(video_path, 'rb')}
            url = HOGHOST + '/api/measurements/{}/video/'.format(measurement_id)
            return requests.put(url, files=files, auth=AUTH).json()
