import time
import logging
from . import dingtalk
from django.http import HttpResponse
from sentry_sdk import capture_exception, capture_message
import traceback

logger = logging.getLogger(__name__)  # __name__当前脚本名称


def performance_logger_middleware(get_response):
    '''中间件'''

    def middleware(request):
        start_time = time.time()
        response = get_response(request)
        duration = time.time() - start_time
        response["X-Page-Duration-ms"] = int(duration * 1000)
        logger.info("%s %s %s" % (duration, request.path, request.GET.dict()))
        return response

    return middleware


class PerformanceAndExceptionLoggerMiddleware:
    '''性能和异常日志记录的中间件'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        response["X-Page-Duration-ms"] = int(duration * 1000)
        logger.info("%s %s %s" % (duration, request.path, request.GET.dict()))
        if duration > 300:
            capture_message("slow request for url:%s with duration:%s" % (request.build_absolute_uri(), duration))

        # Code to be executed for each request/response after
        # the view is called
        return response

    def process_exception(self, request, exception):
        if exception:
            message = "url:{url} ** msg:{error} ````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                # 堆栈信息
                tb=traceback.format_exc(),
            )

            logger.warning(message)

            # send dingtalk message
            dingtalk.send(message)

            # capture exception to sentry
            capture_exception(exception)
        return HttpResponse("Error processing the request,please contact the system administrator.", status=500)
