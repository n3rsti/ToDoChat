from django.urls import re_path

from . import consumers
from users import consumers as users_consumers


websocket_urlpatterns = [
    re_path(r'ws/server/(?P<pk>\w+)/(?P<room_name>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/chat/(?P<id>\w+)/', users_consumers.ChatConsumer),
]