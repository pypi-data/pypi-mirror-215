from big_thing_py.big_thing import *
import subprocess
import pytest


@static_vars(test_var=0)
def func1__test_static_vars():
    func1__test_static_vars.test_var += 1
    return func1__test_static_vars.test_var


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(),
     1, None),
    ('', dict(),
     2, None),
    ('', dict(),
     3, None),
    ('', dict(),
     4, None),
    ('', dict(),
     5, None),
])
def test_static_vars(test_id: str, input: Dict, expected_output: int, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = func1__test_static_vars(**input)
    else:
        output = func1__test_static_vars(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('test1', dict(typ=int),
     'int', None),
    ('test2', dict(typ=str),
     'str', None),
    ('test3', dict(typ=typing.List[str]),
     'list[str]', None),
    ('test4', dict(typ=typing.Dict[str, int]),
     'dict[str, int]', None),
    ('test5', dict(typ=typing.Tuple[int, str]),
     'tuple[int, str]', None),
])
def test_get_type_name(test_id: str, input: Dict[str, type], expected_output: str, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = get_type_name(**input)
    else:
        output = get_type_name(**input)
        assert output == expected_output

####################################################################################################################################


def func1__test_get_function_info(a: int, b: str, c: List[float]) -> str:
    pass


def func2__test_get_function_info(x: str = "default", y: int = 0) -> int:
    pass


def func3__test_get_function_info(a: List[Dict[str, Union[str, int]]], b: Tuple[Union[int, float], str]) -> List[str]:
    pass


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(func=func1__test_get_function_info),
     dict(name='func1__test_get_function_info', args=[('a', int), ('b', str), ('c', List[float])], return_type='str'), None),
    ('', dict(func=func2__test_get_function_info),
     dict(name='func2__test_get_function_info', args=[('x', str), ('y', int)], return_type='int'), None),
    ('', dict(func=func3__test_get_function_info),
     dict(name='func3__test_get_function_info', args=[('a', List[Dict[str, Union[str, int]]]), ('b', Tuple[Union[int, float], str])], return_type='list[str]'), None),
])
def test_get_function_info(test_id: str, input: Dict[str, Callable], expected_output: Dict, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = get_function_info(**input)
    else:
        output = get_function_info(**input)
        assert output == expected_output

####################################################################################################################################


def upper_func__test_get_current_function_name():
    def inner_func():
        return get_current_function_name()
    return inner_func()


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(),
     'inner_func', None),
])
def test_get_current_function_name(test_id: str, input: Dict, expected_output: str, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = upper_func__test_get_current_function_name(**input)
    else:
        output = upper_func__test_get_current_function_name(**input)
        assert output == expected_output

####################################################################################################################################


def upper_func__test_get_upper_function_name(step: int):
    def inner_func1():
        def inner_func2():
            def inner_func3():
                def inner_func4():
                    def inner_func5():
                        return get_upper_function_name(step=step)
                    return inner_func5()
                return inner_func4()
            return inner_func3()
        return inner_func2()
    return inner_func1()


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(step=1),
     'inner_func4', None),
    ('', dict(step=2),
     'inner_func3', None),
    ('', dict(step=3),
     'inner_func2', None),
    ('', dict(step=4),
     'inner_func1', None),
    ('', dict(step=5),
     'upper_func__test_get_upper_function_name', None),
])
def test_get_upper_function_name(test_id: str, input: Dict[str, int], expected_output: str, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = upper_func__test_get_upper_function_name(**input)
    else:
        output = upper_func__test_get_upper_function_name(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(interface=None),
     None, None),
])
def test_get_mac_address(test_id: str, input: Dict[str, str], expected_output: Dict, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = get_mac_address(**input)
    else:
        output: str = get_mac_address(**input)
        assert len(output) == 12
        assert output.isalnum()
        assert output.isupper()

####################################################################################################################################


def test_get_current_time():
    result = get_current_time(TimeFormat.UNIXTIME)
    cur_time = time.time()
    assert isinstance(result, float)
    assert result - cur_time < 0.0001

    result = get_current_time(TimeFormat.DATETIME1)
    assert isinstance(result, str)
    assert len(result) == 19

    result = get_current_time(TimeFormat.DATETIME2)
    assert isinstance(result, str)
    assert len(result) == 15

    result = get_current_time(TimeFormat.DATE)
    assert isinstance(result, str)
    assert len(result) == 10

    result = get_current_time(TimeFormat.TIME)
    assert isinstance(result, str)
    assert len(result) == 8

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(in_type=MXType.INTEGER),
     int, None),
    ('', dict(in_type=MXType.DOUBLE),
     float, None),
    ('', dict(in_type=MXType.BOOL),
     bool, None),
    ('', dict(in_type=MXType.STRING),
     str, None),
    ('', dict(in_type=MXType.BINARY),
     str, None),
    ('', dict(in_type=MXType.VOID),
     None, None),
    ('', dict(in_type=MXType.UNDEFINED),
     None, None),

    ('', dict(in_type=int),
     MXType.INTEGER, None),
    ('', dict(in_type=float),
     MXType.DOUBLE, None),
    ('', dict(in_type=bool),
     MXType.BOOL, None),
    ('', dict(in_type=str),
     MXType.STRING, None),
    ('', dict(in_type=None),
     MXType.VOID, None),
    ('', dict(in_type=type(None)),
     MXType.VOID, None),

    ('', dict(in_type='int'),
     MXType.INTEGER, None),
    ('', dict(in_type='double'),
     MXType.DOUBLE, None),
    ('', dict(in_type='bool'),
     MXType.BOOL, None),
    ('', dict(in_type='string'),
     MXType.STRING, None),
    ('', dict(in_type='binary'),
     MXType.BINARY, None),
    ('', dict(in_type='void'),
     MXType.VOID, None),
    ('', dict(in_type='undefined'),
     MXType.UNDEFINED, None),
])
def test_type_converter(test_id: str, input: Dict[str, Union[MXType, type, str]], expected_output: Union[MXType, type], expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = type_converter(**input)
    else:
        output = type_converter(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(),
     subprocess.check_output('git rev-parse --show-toplevel', shell=True).decode('utf-8').strip(), None),
])
def test_get_project_root(test_id: str, input: Dict, expected_output: str, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = get_project_root(**input)
    else:
        output = get_project_root(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('check_valid_id_1', dict(identifier='test_string1'),
     True, None),
    ('check_valid_id_2', dict(identifier='test_string_1'),
     True, None),
    ('check_valid_id_3', dict(identifier='_test_string_1'),
     True, None),
    ('check_valid_id_4', dict(identifier='1_test_string'),
     False, None),
    ('check_valid_id_5', dict(identifier='test-string'),
     False, None),
    ('check_valid_id_6', dict(identifier='test string'),
     False, None),
    ('check_valid_id_7', dict(identifier=''),
     False, None),
])
def test_check_valid_identifier(test_id: str, input: Dict[str, str], expected_output: bool, expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = check_valid_identifier(**input)
    else:
        output = check_valid_identifier(**input)
        assert output == expected_output

####################################################################################################################################


@pytest.mark.parametrize('test_id, input, expected_output, expected_exception_message', [
    ('', dict(url='localhost'),
     '127.0.0.1', None),
    ('', dict(url='127.0.0.1'),
     '127.0.0.1', None),
    ('', dict(url='123.123.123.123'),
     '123.123.123.123', None),
    ('', dict(url='123.123.123.1234'),
     Exception(), None),
    ('', dict(url='123.123.123.-1'),
     Exception(), None),
])
def test_convert_url_to_ip(test_id: str, input: Union[str, str], expected_output: Union[Dict, Exception], expected_exception_message: str):
    if isinstance(expected_output, Exception):
        with pytest.raises(type(expected_output), match=expected_exception_message):
            output = convert_url_to_ip(**input)
    else:
        output = convert_url_to_ip(**input)
        assert output == expected_output

####################################################################################################################################


def test_check_python_version():
    if sys.version_info[0] <= 3 and sys.version_info[1] < 6:
        with pytest.raises(Exception):
            check_python_version()
    else:
        assert check_python_version() == None

####################################################################################################################################


if __name__ == '__main__':
    pytest.main(['-s', '-vv', __file__])
