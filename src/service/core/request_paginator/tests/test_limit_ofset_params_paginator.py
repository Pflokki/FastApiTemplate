import pytest

from service.core.request_paginator.limit_offset_paginator import LimitOffsetParamsPaginator
from service.core.request_data import RequestData


@pytest.mark.parametrize(
    ('start_offset', 'max_offset', 'limit', 'limit_field_name', 'offset_field_name', 'expected_offset_list'),
    (
        (0, 30, 10, 'limit', 'offset', [0, 10, 20]),
        (0, 30, 10, 'left', 'right', [0, 10, 20]),
        (0, 25, 10, 'limit', 'offset', [0, 10]),
        (5, 35, 10, 'limit', 'offset', [5, 15, 25]),
        (5, 30, 10, 'limit', 'offset', [5, 15]),
    ),
)
def test_limit_offset_params_paginator(
        start_offset, max_offset, limit,
        limit_field_name, offset_field_name,
        expected_offset_list,
):
    rd = RequestData(
        url='test',
        method='get',
        params={'value': 'test'},
    )

    paginator = LimitOffsetParamsPaginator(
        request_data=rd,
        start_offset=start_offset,
        max_offset=max_offset,
        limit=limit,
        limit_field_name=limit_field_name,
        offset_field_name=offset_field_name,
    )

    for current_offset, paginated_request in zip(
            expected_offset_list,
            paginator.get_paginated_request()
    ):
        assert isinstance(paginated_request, RequestData)
        assert paginated_request.params[limit_field_name] == limit
        assert paginated_request.params[offset_field_name] == current_offset
        assert 'value' in paginated_request.params
