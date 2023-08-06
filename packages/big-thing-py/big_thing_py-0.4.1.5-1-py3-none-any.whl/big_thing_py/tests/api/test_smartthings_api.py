from big_thing_py.utils.api_util import *
from big_thing_py.utils.json_util import *
from secret import *


api_token = SMARTTHINS_API_TOKEN

url = "https://api.smartthings.com/v1"
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json;charset-UTF-8'
}
payload_on = {
    'commands': [
        {
            'component': 'main',
            'capability': 'switch',
            'command': 'on',
            'arguments': []
        }
    ]
}
payload_off = {
    'commands': [
        {
            'component': 'main',
            'capability': 'switch',
            'command': 'off',
            'arguments': []
        }
    ]
}
payload_set_brightness = {
    'commands': [
        {
            'component': 'main',
            'capability': 'switchLevel',
            'command': 'setLevel',
            'arguments': [128]
        }
    ]
}


def get_location_list():
    res = API_request(url=f'{url}/locations',
                      method=RequestMethod.GET, header=headers)
    location_list = res['items']
    location_detail_list = []

    for location in location_list:
        location_detail = API_request(
            url=f'{url}/locations/{location["locationId"]}', method=RequestMethod.GET, header=headers)
        location_detail_list.append(location_detail)

    return location_detail_list


def get_location_room_list():
    location_list = get_location_list()

    for location in location_list:
        res = API_request(
            url=f'{url}/locations/{location["locationId"]}/rooms', method=RequestMethod.GET, header=headers)
        room_list = res['items']
        print(room_list)


def get_device_list():
    ret = API_request(
        url=f'{url}/devices', method=RequestMethod.GET, header=headers)
    device_list = ret['items']
    print(device_list)


def get_location_info(location_id: str):
    ret = API_request(
        url=f'{url}/locations/{location_id}', method=RequestMethod.GET, header=headers)
    location_info = ret
    print(location_info)


def get_room_info(location_id: str, room_id: str):
    ret = API_request(
        url=f'{url}/locations/{location_id}/rooms/{room_id}', method=RequestMethod.GET, header=headers)
    room_info = ret
    print(room_info)


if __name__ == '__main__':
    get_location_room_list()
    get_device_list()
    # get_location_info('')
    # get_room_info('', '')
    # get_device_status()
    # control_device_on()
    # control_device_off()
    # control_device_set_brightness()
