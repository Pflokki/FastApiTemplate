from log_formatter.http_service_formatter import HTTPServiceFormatter, LogFormatter

from settings import get_logger

logger = get_logger('http_service')


class BaseServiceLoggerMixin:
    @staticmethod
    def _log_representation_exception(error):
        log_data = LogFormatter(f'Error while decode data from response | {error}')
        logger.error(log_data.get_json_record())

    @staticmethod
    def _log_retry_exception(error, request_data, retry_count):
        log_data = HTTPServiceFormatter(
            message=f'Warning, error {type(error)} while sending request, '
                    f'retry count {retry_count}...',
            request=request_data,
        )
        logger.info(log_data.get_json_record())

    @staticmethod
    def _log_base_send_request_exception(error, request_data):
        log_data = HTTPServiceFormatter(
            message=f'Error {type(error)} while sending request',
            request=request_data,
        )
        logger.info(log_data.get_json_record())

    @staticmethod
    def _log_request(request_data):
        log_data = HTTPServiceFormatter(
            message='Sending request',
            request=request_data,
        )
        logger.info(log_data.get_json_record())

    @staticmethod
    def _log_response(request_data, response_data):
        log_data = HTTPServiceFormatter(
            message='Response received',
            request=request_data,
            response=response_data,
        )
        logger.info(log_data.get_json_record())
