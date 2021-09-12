import time
from django.utils.deprecation import MiddlewareMixin
import logging


logger = logging.getLogger('request_times')

class RequestTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):        

        duration = time.time() - request.start_time
        msg = f"{duration:06.3f} secs : {request.method} - {request.path}"

        logger.debug(msg)        
        return response

