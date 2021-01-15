"""
WSGI config for quantumapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import quantumforum.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.settings')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantumapp.settings')

# application = get_wsgi_application()


application = ProtocolTypeRouter({
  "http": get_wsgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            quantumforum.routing.websocket_urlpatterns
        )
    ),
})
