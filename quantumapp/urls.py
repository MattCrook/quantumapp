from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from quantumapi.models import *

from quantumapi.views import register_user, login_user
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message

from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from quantumapi.auth.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

# from quantumapi.views import Credits

from rest_framework import views, serializers, status
from rest_framework.response import Response


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'parks', Parks, 'park')
router.register(r'tracktypes', Tracktypes, 'tracktype')
router.register(r'manufacturers', Manufacturers, 'manufacturer')
router.register(r'rollercoasters', RollerCoasters, 'rollercoaster')
router.register(r'userprofiles', UserProfiles, 'userprofile')
# router.register(r'credits', Credits, 'credit')
router.register(r'messages', Message, 'message')




#echo API endpoint, to test calls from our front-end...when we would be authorized.
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('api-token-auth/', obtain_auth_token),

    # path('api-token-auth/', obtain_jwt_token),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api-token-refresh/', refresh_jwt_token),
    # path('api-token-verify/', verify_jwt_token),

    # path('register/', register_user),
    # path('login/', login_user),

    # path('', include('quantumapi.urls'))

    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)),
    url(r'^api/$', get_schema_view()),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
]
