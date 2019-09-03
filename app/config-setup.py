import json
import requests

open('/home/pi/config.json', 'w').write('{}')
config = json.load(open('/home/pi/config.json', 'r'))

def get_box_id():
    response = requests.get('http://trinity-stroud.hedgehogrepublic.org/api/locations/').json()
    location_list = response['results']
    for i in location_list:
        print(i['name'])
    box_name = input('Box Name (Must be one of the above): ')
    is_valid = False
    for i in location_list:
        if box_name == i['name']:
            is_valid = True
            config['box_id'] = i['code']
            print('Box name was correct and the box id has been saved')
    return is_valid


def main():
    print('Welcome to the HogPi Setup')
    is_valid = get_box_id()
    if is_valid == False:
        print('The box name you entered is incorrect, please try again')
        get_box_id()

if __name__ == '__main__':
    main()
