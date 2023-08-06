from big_thing_py.utils.api_util import *
from big_thing_py.utils.json_util import *
from secret import *

# eb65ca597dbc149d4esv4q"  # 교수님 방
# ebe63735f2ce316932alsq"  # 미팅룸
# ebaa42dd164ccc48cdhbjf"  # 걸리버

url_scan_whole_devices = "https://goqual.io/openapi/devices"  # 걸리버
url_scan_homes = "https://goqual.io/openapi/homes"  # 걸리버
url_scan_rooms = "https://goqual.io/openapi/homes/%s/rooms"  # 걸리버
url_scan_devices = "https://goqual.io/openapi/homes/%s/rooms/%s/devices"
url_control = "https://goqual.io/openapi/control/ebaa42dd164ccc48cdhbjf"  # 걸리버
api_token = HEJHOME_API_TOKEN

# '63656843'
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json;charset-UTF-8'
}


def get_home_list():
    payload = None
    response = API_request(url_scan_homes, method=RequestMethod.GET,
                           header=headers, body=payload)
    print(response)

    for home in response['result']:
        get_room_list(home['homeId'])


def get_room_list(homeId):
    payload = None
    response = API_request(url_scan_rooms % (homeId), method=RequestMethod.GET,
                           header=headers, body=payload)
    print(response)

    for room in response['rooms']:
        get_device_list(homeId, room['room_id'])


def get_device_list(homeId, roomId):
    payload = None
    response = API_request(url_scan_devices % (homeId, roomId), method=RequestMethod.GET,
                           header=headers, body=payload)
    print(response)


def get_whole_device_list():
    payload = None
    response = API_request(url_scan_whole_devices, method=RequestMethod.GET,
                           header=headers, body=payload)
    print(response)


def get_whole_device_list_recursive():
    payload = None
    device_list = []
    ret = API_request(url_scan_homes, method=RequestMethod.GET,
                      header=headers, body=payload)
    home_list = ret['result']
    for home in home_list:
        home_id = home['homeId']
        ret = API_request(url_scan_rooms % (home_id), method=RequestMethod.GET,
                          header=headers, body=payload)
        room_list = ret['rooms']
        for room in room_list:
            room_id = room['room_id']
            ret = API_request(url_scan_devices % (home_id, room_id), method=RequestMethod.GET,
                              header=headers, body=payload)
            device_list.append(ret)
    print(device_list)


def control_light():
    payload = dict_to_json_string({
        "requirments": {
            "power1": False,
            "power2": False,
            "power3": False,
        }
    })
    response = API_request(url_control, method=RequestMethod.POST,
                           header=headers, body=payload)
    print(response)


if __name__ == '__main__':
    get_whole_device_list_recursive()
