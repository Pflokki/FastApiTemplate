from typing import Generator
from copy import deepcopy

from service.core.request_paginator.base_paginator import Paginator
from service.core.request_data import RequestData


class LimitOffsetParamsPaginator(Paginator):
    def __init__(
            self,
            request_data: RequestData,
            start_offset: int,
            max_offset: int,
            limit: int,
            limit_field_name: str = 'limit',
            offset_field_name: str = 'offset',
    ):
        super(LimitOffsetParamsPaginator, self).__init__(request_data)

        self.start_offset: int = start_offset
        self.max_offset: int = max_offset
        self.limit: int = limit

        self._limit_field_name: str = limit_field_name
        self._offset_field_name: str = offset_field_name

    def get_paginated_request(self) -> Generator[RequestData, None, None]:
        if not self.request_data.params:
            self.request_data.params = {}
        self.request_data.params[self._limit_field_name] = self.limit

        for offset in range(
                self.start_offset,
                self.max_offset + self.limit,
                self.limit
        ):
            self.request_data.params[self._offset_field_name] = offset

            yield deepcopy(self.request_data)
