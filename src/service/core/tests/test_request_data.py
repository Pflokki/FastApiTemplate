from service.core.request_data import RequestData


def test_request_data_parse_ant_data():
    rd = RequestData(url='url', method='get', data='string')
    assert rd.json is None and rd.data == 'string'


def test_request_data_parse_dict_data():
    rd = RequestData(url='url', method='get', data={})
    assert rd.data is None and rd.json == {}


def test_request_data_get_dict_include_none():
    rd = RequestData(url='url', method='get', data={})

    expected_dict = dict(
        url=rd.url,
        params=rd.params,
        headers=rd.headers,
        data=rd.data,
        json=rd.json,
        auth=rd.auth,
    )

    assert rd.to_dict(exclude_none=False) == expected_dict


def test_request_data_get_dict_exclude_none():
    rd = RequestData(url='url', method='get', data={'value': 'value'})

    expected_dict = dict(
        url=rd.url,
        json=rd.json,
    )

    assert rd.to_dict(exclude_none=True) == expected_dict
