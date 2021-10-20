"""
ASGI config for quantumapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os
# import django
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import quantumforum.routing



application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "https": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            quantumforum.routing.websocket_urlpatterns
        )
    ),
})
