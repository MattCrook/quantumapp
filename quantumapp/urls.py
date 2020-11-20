from django.contrib import admin
from rest_auth.registration.views import ConfirmEmailView
from rest_framework.response import Response
from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message, Credits, Users, Images, Credentials
from quantumapi.views import login_user, register_user, get_user
from quantumapi.views import Auth0Data as Auth0DataView


# from quantumapi.models import *
# from allauth.account.views import confirm_email
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt import views as jwt_views
# from django.views import generic
# from quantumapi import urls

# python manage.py dumpdata > /Users/matthewcrook/code/nss/frontEnd/quantumapp/quantumapi/fixtures/datadump.json

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
router.register(r'auth0data', Auth0DataView, 'auth0data')
router.register(r'credentials', Credentials, 'credentials')



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest-auth/login/', login_user),
    path('rest-auth/registration/', register_user),
    path('rest-auth/', include('rest_auth.urls')),
    path('account/', include('allauth.urls')),
    url(r'^rest-auth/registration/verify-email/(?P<key>.+)/$', ConfirmEmailView, name='account_confirm_email'),
    path('get_user/', get_user),
    path('rest-auth/logout/', include('rest_auth.registration.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),

    # path('rest-auth/registration/verify-email/<slug:key>/', confirm_email, name='account_confirm_email'),
    # url(r'^rest-auth/registration/verify-email/', confirm_email, name='account_confirm_email'),
    # path('', include('quantumapi.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
