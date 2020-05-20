"""quantumapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from quantumapi.models import *
from quantumapi.views import register_user, login_user
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'parks', Parks, 'park')
router.register(r'tracktypes', Tracktypes, 'tracktype')
router.register(r'manufacturers', Manufacturers, 'manufacturer')
router.register(r'rollercoasters', RollerCoasters, 'rollercoaster')
router.register(r'userprofiles', UserProfiles, 'userprofile')
# router.register(r'credits', Credits, 'credit')
router.register(r'messages', Message, 'credit')



urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', register_user),
    path('login/', login_user),
]
