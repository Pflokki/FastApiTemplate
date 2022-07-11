from service.core.response_data import ResponseData, StatusCodes


def test_request_data_get_data():
    rd = ResponseData(
        status=StatusCodes.HTTP_200.value,
        data='hello'
    )
    assert rd.get_data() == 'hello' and rd.get_error() == {}


def test_request_data_get_error():
    rd = ResponseData(
        status=StatusCodes.HTTP_500.value,
        data='hello'
    )
    assert rd.get_data() == 'hello' and rd.get_error() == 'hello'
