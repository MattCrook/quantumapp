from django.contrib import admin
from rest_auth.registration.views import ConfirmEmailView
from rest_framework.response import Response
from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message, Credits, Users, Images, News, BlogContributorApplications, ActivityLogView, LoginInfoView, CalendarEvents, ErrorLogView
from quantumapi.views import login_user, register_user, get_user, auth0_logout
from quantumapi.views import Credentials as CredentialsView
from rest_framework.authtoken.views import obtain_auth_token
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
router.register(r'credentials', CredentialsView, 'credentials')
router.register(r'news', News, 'news')
router.register(r'contributor_applications', BlogContributorApplications, 'contributor_application')
router.register(r'activity_log', ActivityLogView, 'activity_log')
router.register(r'login_info', LoginInfoView, 'login_info')
router.register(r'calendar_events', CalendarEvents, 'calendar_event')
router.register(r'error_logs', ErrorLogView, 'error_logs')




urlpatterns = [
    path('', include(router.urls)),
    path('chat/', include('quantumforum.urls')),
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
