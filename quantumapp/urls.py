# from rest_framework.authtoken.views import obtain_auth_token

# JWT DJANGO REST OAUTH
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
# from rest_framework_jwt.utils import jwt_decode_token, jwt_get_username_from_payload_handler

# from quantumapi.auth.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
# from quantumapi.utils import jwt_decode_token, jwt_get_username_from_payload_handler
# from rest_framework.schemas import get_schema_view

from django.contrib import admin
# from django.contrib.auth.views import UserModel

from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from django.views import generic
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt import views as jwt_views
from rest_framework import views, serializers, status
from rest_framework.response import Response
from quantumapi.models import *

from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message, Credits, Users, Images
from quantumapi.views import login_user, register_user, get_user
# from quantumapi import urls

# Auth0 Paths
from quantumapi.utils import jwt_decode_token, jwt_get_username_from_payload_handler


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'parks', Parks, 'park')
router.register(r'tracktypes', Tracktypes, 'tracktype')
router.register(r'manufacturers', Manufacturers, 'manufacturer')
router.register(r'rollercoasters', RollerCoasters, 'rollercoaster')
router.register(r'userprofiles', UserProfiles, 'userprofile')
router.register(r'credits', Credits, 'credit')
router.register(r'messages', Message, 'messages')
router.register(r'users', Users, 'user')
router.register(r'images', Images, 'image')




urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_user),
    path('login/', login_user),
    path('get_user/', get_user),
    path('', include('quantumapi.urls')),
    # path('auth/', include('rest_auth.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api-token-auth/', obtain_auth_token),


    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('', generic.RedirectView.as_view(url='/api/', permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    # path('get_user/', get_user),
    # path('api-token-auth/', obtain_auth_token),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),



    # path('api-token-verify/', verify_jwt_token),
    # path('api-token-auth/', obtain_jwt_token),
    # path('api-token-decode/', jwt_decode_token),
    # path('api-token-refresh/', refresh_jwt_token),


    # AUTH0 PATHS
    # path('', include(jwt_decode_token)),
    # path('', include(jwt_get_username_from_payload_handler)),


    # path('', include('jwt_decode_token')),
    # path('', include('jwt_get_username_from_payload_handler')),
    # path('', include('quantumapi.urls')),

    # path('api/$', get_schema_view()),
    # path('api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    # path('api/auth/token/refresh/$', TokenRefreshView.as_view()),


    # path('register/', register_user),
    # path('login/', login_user),
