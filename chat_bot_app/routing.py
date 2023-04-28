from django.urls import re_path
from .helpers.websocket import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<grpname>\w+)/$', ChatConsumer.as_asgi())
]