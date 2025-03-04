from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/private/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/group/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]