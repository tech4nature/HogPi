import json
import requests

open('/home/pi/config.json', 'w').write('{}')
config = json.load(open('/home/pi/config.json', 'r'))

def get_box_id():
    response = requests.get('http://trinity-stroud.hedgehogrepublic.org/api/locations/').json()
    location_list = response['results']
    i = 0
    for j in location_list:
        i += 1
        print(f'{i}) {j["name"]}')
    box = int(input('Box Number: '))
    config['box_id'] = location_list[box - 1]['code']
    


def main():
    print('Welcome to the HogPi Setup')
    try:
        get_box_id()
    except Exception:
        get_box_id()

if __name__ == '__main__':
    main()
    json.dump(config, open('/home/pi/config.json', 'w'))
