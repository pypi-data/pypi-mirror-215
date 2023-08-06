
from typing import Callable
from scrapy import signals
from scrapy.http import HtmlResponse, TextResponse
from twisted.internet.threads import deferToThread
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.exceptions import IgnoreRequest
from scrapy_manipulate_request.exception import TypeError
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
import logging
logger = logging.getLogger(__name__)


class ManipulateRequestDownloaderMiddleware:

    EXCEPTIONS_TO_RETRY = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
        ResponseFailed,
        IOError,
        TunnelError,
    )
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        s = cls()
        cls.retry_enabled = settings.getbool('RETRY_ENABLED')
        cls.max_retry_times = settings.getint('RETRY_TIMES')
        cls.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        cls.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return cls()

    def _retry(self, request, reason, spider):

        if not self.retry_enabled:
            return None

        retry_times = request.meta.get('retry_times', 0) + 1
        max_retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            max_retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retry_times <= max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retry_times)d times): %(reason)s",
                         {'request': request, 'retry_times': retry_times, 'reason': reason},
                         extra={'spider': spider})
            new_request = request.copy()
            new_request.meta["retry_times"] = retry_times
            new_request.dont_filter = True
            new_request.priority = request.priority + self.priority_adjust

            if callable(reason):
                reason = reason()
            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return new_request
        else:
            stats.inc_value('retry/max_reached')
            logger.error("Gave up retrying %(request)s (failed %(retry_times)d times): %(reason)s",
                         {'request': request, 'retry_times': retry_times, 'reason': reason},
                         extra={'spider': spider})
            return None
    
    def _process_request(self, request, spider):
        manipulate_request = request.meta.get('manipulate_request', lambda: HtmlResponse(url=request.url,
                                        status=404, headers='', body='', request=request, encoding='utf-8'))
        if not isinstance(manipulate_request, Callable):
            raise TypeError(f'manipulate_request should be a function, but {type(request)} received')
        try:
            response = manipulate_request(request, spider)
        except Exception as e:
            return None
        if response is None:
            raise IgnoreRequest
        if not isinstance(response, HtmlResponse) or not isinstance(response, TextResponse):
            raise TypeError(f'response should be a HtmlResponse or TextResponse object,\
                                    but {type(request)} received')
        return response

    def process_request(self, request, spider):
        logger.debug('manipulate_process function process request %s', request)
        return deferToThread(self._process_request, request, spider)

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get(
                "dont_retry", False
        ):
            return self._retry(request, exception, spider)

    def spider_opened(self, spider):
        spider.logger.info("ManipulateRequestDownloaderMiddleware enabled")

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s" % spider.name)


