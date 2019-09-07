import json
import requests


def setup():
    open('/home/pi/config.json', 'w').write('{}')
    config = json.load(open('/home/pi/config.json', 'r'))
    return config
    
def get_box_id(config):
    response = requests.get('http://trinity-stroud.hedgehogrepublic.org/api/locations/').json()
    location_list = response['results']
    i = 0
    for j in location_list:
        i += 1
        print(str(i) + ') ' + j["name"])
    box = int(input('Box Number: '))
    config['box_id'] = location_list[box - 1]['code']
    


def main():
    print('Welcome to the HogPi Setup')
    config = setup()
    try:
        get_box_id(config)
    except Exception:
        print('Invalid value inputed, try again.')
        get_box_id(config)

if __name__ == '__main__':
    main()
    json.dump(config, open('/home/pi/config.json', 'w'))
