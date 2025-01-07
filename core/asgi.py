import os

import django 
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from restaurant.consumers import ReservationUpdateConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/reservation_updates/', ReservationUpdateConsumer.as_asgi())  # Новый путь для бронирований
        ])
    ),
})

