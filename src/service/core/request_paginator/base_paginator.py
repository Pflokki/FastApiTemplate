from abc import ABCMeta, abstractmethod
from service.core.request_data import RequestData


class Paginator(metaclass=ABCMeta):
    def __init__(self, request_data: RequestData):
        self.request_data = request_data

    @abstractmethod
    def get_paginated_request(self):
        pass
