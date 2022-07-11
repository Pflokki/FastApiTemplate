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

    @pytest.mark.parametrize(
        ('retry_count', 'expected_value'),
        [
            (-1, 0),
            (0, 0),
            (3, 3),
        ],
    )
    def test_request_policy_retry_count_value(self, retry_count, expected_value):
        rp = RequestPolicy(retry_count=retry_count)
        assert rp.retry_count == expected_value

    @pytest.mark.parametrize(
        ('retry_count', 'current_retry_count', 'is_need_retry'),
        [
            (0, 0, True),
            (0, 1, False),
            (3, 3, False),
            (3, 2, True),
        ],
    )
    def test_request_policy_retry(self, retry_count, current_retry_count, is_need_retry):
        rp = RequestPolicy(retry_count=retry_count)
        assert rp.is_need_retry(current_retry_count) == is_need_retry

