from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat/<chat_id>/', consumers.ChatConsumer.as_asgi()),
    path(r'ws/profile/<user_id>/', consumers.UserConsumer.as_asgi()),
]