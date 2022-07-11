from service.core.request_paginator.base_paginator import Paginator
from service.core.request_data import RequestData


class AttributePaginator(Paginator):
    def __init__(self, request_data: RequestData):
        super(AttributePaginator, self).__init__(request_data)

    def get_paginated_request(self):
        pass
