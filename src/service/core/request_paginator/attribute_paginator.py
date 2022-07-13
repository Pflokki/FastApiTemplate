from typing import Generator
from enum import Enum
from copy import deepcopy

from service.core.request_paginator.base_paginator import Paginator
from service.core.request_data import RequestData


class RequestAttributes(Enum):
    params = 'params'
    headers = 'headers'
    data = 'json'


class AttributePaginator(Paginator):
    def __init__(
            self,
            request_data: RequestData,
            attribute_name: RequestAttributes,
            attribute_key: str,
            limit: int
    ):
        super(AttributePaginator, self).__init__(request_data)

        self.attribute_name: RequestAttributes = attribute_name
        self.attribute_key: str = attribute_key
        self.limit: int = limit

    def _is_attribute_valid(self):
        if request_attribute := getattr(self.request_data, self.attribute_name.value, {}):
            if isinstance(request_attribute, dict):
                iterable_data: list | tuple = request_attribute.get(self.attribute_key, [])
                if type(iterable_data) in [list, tuple] and len(iterable_data):
                    return True
        return False

    def _paginate_attribute(self, iterable_data: list | tuple):
        left_offset = 0
        for right_offset in range(self.limit, len(iterable_data) + self.limit, self.limit):
            paginated_iterable_data = iterable_data[left_offset:min(right_offset, len(iterable_data))]
            if not getattr(self.request_data, self.attribute_name.value):
                setattr(self.request_data, self.attribute_name.value, {})
            getattr(self.request_data, self.attribute_name.value)[self.attribute_key] = paginated_iterable_data
            yield self.request_data
            left_offset = right_offset

    def get_paginated_request(self) -> Generator[RequestData, None, None]:
        if self._is_attribute_valid():
            request_attribute = getattr(self.request_data, self.attribute_name.value)
            iterable_data: list | tuple = request_attribute.get(self.attribute_key)

            for paginated_request in self._paginate_attribute(iterable_data):
                yield paginated_request

        else:
            yield deepcopy(self.request_data)
