"""
EcoMboa — WSGI Configuration
------------------------------
Exposes the WSGI callable as module-level variable 'application'.
Used by traditional WSGI servers (Gunicorn, uWSGI).
For WebSocket support, use asgi.py instead.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
