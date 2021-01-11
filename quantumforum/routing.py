from django.urls import re_path
from . import consumers

# Pass emial or auth0 ID to URL to get user
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
