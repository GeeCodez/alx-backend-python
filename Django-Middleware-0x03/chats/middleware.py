import logging 
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self,get_response) -> None:
        self.get_response=get_response

        #creating or getting a logger
        self.logger=logging.getLogger('request_logger')
        handler=logging.FileHandler('requests.log')
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
    
class OffensiveLanguageMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

        #dictionary to store request info per ip address
        #format: {"ip_address": [list_of_request_timestamps]}
        self.ip_requests={}

    def __call__(self,request):
        if request.method=="POST" and request.path.startswith("/api/conversation"):
            #get the client ip address
            ip=self.get_client_ip(request)
            now=datetime.now()

            if ip not in self.ip_requests:
                self.ip_requests[ip]=[]
            
            #remove the timestamp older than 1 minute
            one_minute_ago=now-timedelta(minutes=1)
            self.ip_requests[ip]=[t for t in self.ip_requests[ip] if t >one_minute_ago]

            if len(self.ip_requests[ip])>=5:
                return HttpResponseForbidden("You are sending too many messages. Limit is 5 messages per minute")

            self.ip_requests[ip].append(now) 
        
        response=self.get_response(request)
        return 
    
    def get_client_ip(self,request):
        """
        Get the client IP address from the request. 
        Handles cases where app is behing a proxy
        """
        x_forward_for=request.META.get("HTTP_X_FORWARD_FOR")
        if x_forward_for:
            ip=x_forward_for.split(',')[0]
        else:
            ip=request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):
        if request.path.startswith('/api/conversation'):
            user=request.user

            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to perform this action")

            if user.role not in ['admin','moderator']:
                return HttpResponseForbidden("You do not have the permission to perform this action")

        response=self.get_response(request)
        return response
    