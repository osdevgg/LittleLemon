from rest_framework.response import Response
from rest_framework import viewsets

from .models import MenuItem
from .serializers import MenuItemSerializer

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class MenuItemsViewSet(viewsets.ModelViewSet):
# Added public property to throttle in class-based views    
#    throttle_classes = [AnonRateThrottle, UserRateThrottle]
# Supressed for conditional -or by-method- throttling
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# Conditional throttling overriding the get_throttles method
# extending a ModelViewSet class, the POST call is handled by create methods.
# Similarly, the GET call is handled by the list method
# Instead, this checks if the router called the create action, which handles the POST request.
# If that action is called, implement the throttling class UserRateThrottle whose throttling rate
# seems to be defined in settings.py
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = [] 
        return [throttle() for throttle in throttle_classes]
    
# You can also use the custom throttling classes you created earlier in the course, 
# like TenCallsPerMinute in the throttles.py file. 
# All you have to do is import this class and then add it in the throttle_classes attribute:
# from .throttles import TenCallsPerMinute
# and then
# throttle_classes = [TenCallsPerMinute]

# Real world examples of API rate limits:
# Here are some popular services and their current rate limit. 
# This can help you to get some idea of how others are using such features in their API projects.

#Service               Anonymous     Authenticated
#Facebook graph API          X           200/hour
#Instagram API               X           200/hour
#Instagram messenger API     X           100/second
#WhatsApp messaging API      X           80/second