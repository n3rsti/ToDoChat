from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/server/(?P<pk>\w+)/channel/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]