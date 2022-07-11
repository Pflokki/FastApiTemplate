import pytest

from service.core.request_data import RequestData
from service.core.response_data import ResponseData
from log_formatter.http_service_formatter import HTTPServiceFormatter


@pytest.fixture()
def request_data():
    request_url = 'url'
    request_method = 'get'
    request_params = {'value': 'test'}

    return RequestData(request_url, request_method, request_params)


@pytest.fixture()
def response_data():
    response_status = 300
    response_data = 'hello'

    return ResponseData(status=response_status, data=response_data)


def test_base_log_string_formatter_with_response(request_data: RequestData, response_data: ResponseData):
    message = 'message'

    log_str = f'message={message}, request_url={request_data.url}, request_method={request_data.method}, ' \
              f'request_params={request_data.params}, request_headers={request_data.headers}, ' \
              f'request_data={request_data.data}, response_status={response_data.status}, ' \
              f'response_data={response_data.get_data()}'

    log_formatter = HTTPServiceFormatter(message=message, request=request_data, response=response_data)
    assert log_formatter.get_str_record() == log_str


def test_base_log_dict_formatter_with_response(request_data: RequestData, response_data: ResponseData):
    message = 'message'

    log_dict = {
        'message': message,

        'request_url': request_data.url,
        'request_method': request_data.method,
        'request_params': request_data.params,
        'request_headers': request_data.headers,
        'request_data': request_data.data,

        'response_status': response_data.status,
        'response_data': response_data.get_data(),
    }

    log_formatter = HTTPServiceFormatter(message=message, request=request_data, response=response_data)
    assert log_formatter.get_dict_record() == log_dict


def test_base_log_string_formatter_without_response(request_data: RequestData):
    message = 'message'

    log_str = f'message={message}, request_url={request_data.url}, request_method={request_data.method}, ' \
              f'request_params={request_data.params}, request_headers={request_data.headers}, ' \
              f'request_data={request_data.data}, response_status=500, response_data={{}}'

    log_formatter = HTTPServiceFormatter(message=message, request=request_data)
    assert log_formatter.get_str_record() == log_str


def test_base_log_dict_formatter_without_response(request_data: RequestData):
    message = 'message'

    log_dict = {
        'message': message,

        'request_url': request_data.url,
        'request_method': request_data.method,
        'request_params': request_data.params,
        'request_headers': request_data.headers,
        'request_data': request_data.data,

        'response_status': 500,
        'response_data': {},
    }

    log_formatter = HTTPServiceFormatter(message=message, request=request_data)
    assert log_formatter.get_dict_record() == log_dict
