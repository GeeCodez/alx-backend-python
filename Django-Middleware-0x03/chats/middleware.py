import logging 
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self,get_response) -> None:
        self.get_response=get_response

        #creating or getting a logger
        self.logger=logging.getLogger('request_logger')
        handler=logging.FileHandler('request_logs.log')
        formatter=logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)


    def __call__(self,request):
        user=request.user if request.user.is_authenticated else "Anonymous"

        log_message=f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response=self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        #check if the user is trying to access the chat
        if request.path.startswith('api/conversation/'):
            current_hour=datetime.now().hour

            if current_hour>=21 or current_hour<6:
                return HttpResponseForbidden("Chat is only available between 6AM AND 9PM")
        
        response=self.get_response(request)
        return response