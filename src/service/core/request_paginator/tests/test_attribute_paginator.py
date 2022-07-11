import pytest

from service.core.request_paginator.attribute_paginator import AttributePaginator, RequestAttributes
from service.core.request_data import RequestData


@pytest.mark.parametrize(
    ('attribute_name', 'attribute_key', 'attribute_list_length', 'limit'),
    (
        (RequestAttributes.params, 'test_values', 15, 10),
        (RequestAttributes.headers, 'test_values', 15, 10),
        (RequestAttributes.data, 'test_values', 15, 10),
        (RequestAttributes.data, 'test_values', 20, 10),
        (RequestAttributes.data, 'test_values', 5, 10),
    ),
)
def test_limit_offset_params_paginator(attribute_name, attribute_key, attribute_list_length, limit):
    rd = RequestData(
        url='test',
        method='get',
        params={},
        headers={},
        data={},
    )
    getattr(rd, attribute_name.value)[attribute_key] = list(range(attribute_list_length))

    paginator = AttributePaginator(
        request_data=rd,
        attribute_name=attribute_name,
        attribute_key=attribute_key,
        limit=limit,
    )

    paginated_list = []
    for paginated_request in paginator.get_paginated_request():
        assert isinstance(paginated_request, RequestData)

        paginated_attribute_list = getattr(paginated_request, attribute_name.value).get(attribute_key)
        assert len(paginated_attribute_list) <= limit

        paginated_list.extend(paginated_attribute_list)

    assert len(paginated_list) == attribute_list_length
