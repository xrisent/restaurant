import os

import django 
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Set the settings before importing anything else

from restaurant.consumers import TableUpdateConsumer
from django.urls import re_path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/table_updates/', TableUpdateConsumer.as_asgi())
        ])
    ),
})
