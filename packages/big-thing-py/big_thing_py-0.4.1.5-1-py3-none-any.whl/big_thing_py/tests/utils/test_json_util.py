from big_thing_py.big_thing import *
import pytest


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(json_string='{"key1": 1, "key2": "1", "key3": 1.1, "key4": true, "key5": false, "key6": null, "key7": [1, 2, 3], "key8": {"key8_1": 1, "key8_2": 2}}'),
     {'key1': 1, 'key2': '1', 'key3': 1.1, 'key4': True, 'key5': False, 'key6': None, 'key7': [1, 2, 3], 'key8': {'key8_1': 1, 'key8_2': 2}}, None),
    ('', dict(json_string='not json string'),
     'not json string', None),
])
def test_json_string_to_dict(test_id: str, input: str, expected_output: Union[str, Exception], expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=None):
            output = json_string_to_dict(**input)
    else:
        output = json_string_to_dict(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(dict_object={'key1': 1, 'key2': '1', 'key3': 1.1, 'key4': True, 'key5': False, 'key6': None, 'key7': [1, 2, 3], 'key8':{'key8_1': 1, 'key8_2': 2}}, pretty=True, indent=4),
     '{\n    "key1": 1,\n    "key2": "1",\n    "key3": 1.1,\n    "key4": true,\n    "key5": false,\n    "key6": null,\n    "key7": [\n        1,\n        2,\n        3\n    ],\n    "key8": {\n        "key8_1": 1,\n        "key8_2": 2\n    }\n}', None),
    ('', dict(dict_object={'key1': 1, 'key2': '1', 'key3': 1.1, 'key4': True, 'key5': False, 'key6': None, 'key7': [1, 2, 3], 'key8':{'key8_1': 1, 'key8_2': 2}}, pretty=True, indent=2),
     '{\n  "key1": 1,\n  "key2": "1",\n  "key3": 1.1,\n  "key4": true,\n  "key5": false,\n  "key6": null,\n  "key7": [\n    1,\n    2,\n    3\n  ],\n  "key8": {\n    "key8_1": 1,\n    "key8_2": 2\n  }\n}', None),
    ('', dict(dict_object={'key1': 1, 'key2': '1', 'key3': 1.1, 'key4': True, 'key5': False, 'key6': None, 'key7': [1, 2, 3], 'key8':{'key8_1': 1, 'key8_2': 2}}, pretty=False),
     '{"key1": 1, "key2": "1", "key3": 1.1, "key4": true, "key5": false, "key6": null, "key7": [1, 2, 3], "key8": {"key8_1": 1, "key8_2": 2}}', None),
])
def test_dict_to_json_string(test_id: str, input: str, expected_output: Union[str, Exception], expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=None):
            output = dict_to_json_string(**input)
    else:
        output = dict_to_json_string(**input)
        assert output == expected_output

####################################################################################################################################


if __name__ == '__main__':
    pytest.main(['-s', '-vv', __file__])
