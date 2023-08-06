from big_thing_py.utils.api_util import *
from big_thing_py.utils.json_util import *
from secret import *


def enhance_color(normalized):
    '''
    Convert RGB to Hue color set
    This is based on original code from http://stackoverflow.com/a/22649803
    '''

    import math

    if normalized > 0.04045:
        return math.pow((normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92


def rgb_to_xy(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = enhance_color(rNorm)
    gFinal = enhance_color(gNorm)
    bFinal = enhance_color(bNorm)

    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0, 0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)

        return [xFinal, yFinal]


api_token = HUE_API_TOKEN

endpoint = f'http://147.46.114.165/api'
endpoint_v2 = f'http://147.46.114.165/clip/v2'
get_all_light_url = f'{endpoint}/{api_token}/lights'
get_new_light_url = f'{endpoint}/{api_token}/lights/new'
get_all_sensor_url = f'{endpoint}/{api_token}/sensors'
get_new_sensor_url = f'{endpoint}/{api_token}/sensors/new'
url_v2 = f'{endpoint_v2}/resource/light'

header = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json;charset-UTF-8'
}
header_v2 = {
    'hue-application-key': api_token
}


def test_get_all_lights():
    response = API_request(
        get_all_light_url, method=RequestMethod.GET, header=header)
    print(response)


def test_get_all_sensors():
    response = API_request(
        get_all_sensor_url, method=RequestMethod.GET, header=header)
    print(response)


def test_get_all_lights_v2():
    response = API_request(
        f'{endpoint_v2}/resource/device', method=RequestMethod.GET, header=header_v2)
    print(response)


def test_control_light():
    # hue light on test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'on': False}),
        header=header)
    # hue light off test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'off': False}),
        header=header)
    # hue light set brightness test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'bri': 128}),
        header=header)
    # hue light set color test
    color_rgb = (255, 0, 0)
    x, y = rgb_to_xy(*color_rgb)
    res: requests.Response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'xy': [x, y]}),
        header=header)


def test_control_light_v2():
    # hue light on test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint_v2}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'on': False}),
        header=header_v2)
    # hue light off test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint_v2}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'off': False}),
        header=header_v2)
    # hue light set brightness test
    response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint_v2}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'bri': 128}),
        header=header_v2)
    # hue light set color test
    color_rgb = (255, 0, 0)
    x, y = rgb_to_xy(*color_rgb)
    res: requests.Response = API_request(
        method=RequestMethod.POST,
        url=f'{endpoint_v2}/{api_token}/lights/{1}/state',
        body=dict_to_json_string({'xy': [x, y]}),
        header=header_v2)


if __name__ == '__main__':
    test_get_all_lights()
    test_control_light()
