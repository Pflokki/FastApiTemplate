import pytest

from aiohttp.client_exceptions import ClientPayloadError

from service.core.base import RequestPolicy


class TestRequestPolicy:
    @pytest.fixture(scope='class')
    def request_policy(self):
        return RequestPolicy(timeout=5, retry_count=0)

    def test_request_policy_add_retry_reason(self, request_policy):
        request_policy.add_retry_reason(ClientPayloadError)
        assert ClientPayloadError in request_policy.retry_reason

    def test_request_policy_add_retry_status_codes(self, request_policy):
        request_policy.add_retry_status_codes([200, ])
        assert 200 in request_policy.retry_status_codes