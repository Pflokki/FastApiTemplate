import ujson

from log_formatter.base import LogFormatter


def test_base_log_string_formatter():
    message = 'Hello'
    log_str = f'message={message}'

    log_formatter = LogFormatter(message=message)
    assert log_formatter.get_str_record() == log_str


def test_base_log_dict_formatter():
    message = 'Hello'
    log_dict = {'message': message}

    log_formatter = LogFormatter(message=message)
    assert log_formatter.get_dict_record() == log_dict


def test_base_log_json_formatter():
    message = 'Hello'
    log_str = ujson.dumps({'message': message})

    log_formatter = LogFormatter(message=message)
    assert log_formatter.get_json_record() == log_str
