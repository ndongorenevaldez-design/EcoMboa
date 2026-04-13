"""
EcoMboa — ASGI Configuration
------------------------------
Handles both HTTP (Django) and WebSocket (Channels) traffic.
WebSocket routes are used for real-time notifications.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Initialize Django ASGI application first to ensure AppRegistry is populated.
django_asgi_app = get_asgi_application()

# Import websocket URL patterns AFTER Django setup
from apps.notifications.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    # HTTP → standard Django ASGI application
    'http': django_asgi_app,
    # WebSocket → authenticated channel routing
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
