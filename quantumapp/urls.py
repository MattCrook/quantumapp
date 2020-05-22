from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from quantumapi.models import *

from quantumapi.views import register_user, login_user
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message

from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from quantumapi.auth.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

# from quantumapi.views import Credits



router = routers.DefaultRouter(trailing_slash=False)

router.register(r'parks', Parks, 'park')
router.register(r'tracktypes', Tracktypes, 'tracktype')
router.register(r'manufacturers', Manufacturers, 'manufacturer')
router.register(r'rollercoasters', RollerCoasters, 'rollercoaster')
router.register(r'userprofiles', UserProfiles, 'userprofile')
# router.register(r'credits', Credits, 'credit')
router.register(r'messages', Message, 'message')



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('api-token-auth/', obtain_auth_token),

    path('api-token-auth/', obtain_jwt_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),

    path('register/', register_user),
    path('login/', login_user),

    # path('', include('quantumapi.urls'))
]
