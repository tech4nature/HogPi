import logging
import json
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


HOGHOST = "http://trinity-stroud.hedgehogrepublic.org"
with open('/home/pi/password.txt', 'r') as f:
    AUTH = HTTPBasicAuth("tech4nature", f.read()[:12])


logger = logging.getLogger(__name__)


def create_location(code, name):
    data = {"code": code, "name": name}

    return requests.post(HOGHOST + "/api/locations/", data=data, auth=AUTH).json()


def _create_measurement(
    location_id, measurement_type, time, measurement=None, hog_id=None
):
    data = {
        "hog_id": hog_id,
        "measurement_type": measurement_type,
        "observed_at": time.isoformat(),
        "location_id": location_id,
    }
    if measurement is not None:
        data["measurement"] = measurement

    response = requests.post(HOGHOST + "/api/measurements/", data=data, auth=AUTH)
    response.raise_for_status()
    return response.json()


def create_weight(location_id, hog_id, weight, time):
    return _create_measurement(location_id, "weight", time, weight, hog_id)


def create_inside_temp(location_id, temp, time):
    return _create_measurement(location_id, "in_temp", time, temp)


def create_outside_temp(location_id, temp, time):
    return _create_measurement(location_id, "out_temp", time, temp)


def upload_video(location_id, hog_id, video_path, time):
    measurement = _create_measurement(location_id, "video", time, hog_id=hog_id)
    logger.debug(measurement)
    measurement_id = measurement["id"]
    files = {"video": open(video_path, "rb")}
    url = HOGHOST + "/api/measurements/{}/video/".format(measurement_id)
    response =  requests.put(url, files=files, auth=AUTH)
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    username = input("username:")
    password = input("password:")
    AUTH = HTTPBasicAuth(username, password)

    print("Making a location:")
    print(create_location("myplace", "My place"))
    print()
    print("Adding a weight:")
    print(create_weight("myplace", "hog-23", 320.5))
    print()
    print("Adding inside and outside temperatures:")
    print(create_inside_temp("myplace", 19.0))
    print(create_outside_temp("myplace", 18.4))
    print()
    print("Adding a video:")
    print(upload_video("myplace", "hog-23", "hog/media/sample_file.mp4"))
    print()
    print("All data for My Place")
    print(
        json.dumps(
            requests.get(HOGHOST + "/api/measurements/?location=myplace").json(),
            indent=2,
        )
    )
