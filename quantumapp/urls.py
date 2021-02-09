from django.contrib import admin
from rest_auth.registration.views import ConfirmEmailView
from rest_framework.response import Response
from rest_framework import routers
from django.conf.urls import url, include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message, Credits, Users, Images, News, BlogContributorApplications, ActivityLogView, LoginInfoView, CalendarEvents, ErrorLogView, AppLoginDataView, GroupChatApiView
from quantumapi.views import login_user, register_user, get_user, auth0_logout
from quantumapi.views import Credentials as CredentialsView
from quantumapi.views import Feedback as FeedbackView
from quantumapi.views import BugReports as BugReportView
from quantumforum.views import FriendRequests as FriendRequestView
from quantumforum.views import StatusCodes as StatusCodeView
from quantumforum.views import Friendships as FriendshipView
from rest_framework.authtoken.views import obtain_auth_token


app_name = "quantumapp"


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
router.register(r'user_feedback', FeedbackView, 'user_feedback')
router.register(r'bug_reports', BugReportView, 'bug_reports')
router.register(r'status_code', StatusCodeView, 'status_codes')
router.register(r'friend_requests', FriendRequestView, 'friend_request')
router.register(r'friendships', FriendshipView, 'friendship')
router.register(r'app_login_data', AppLoginDataView, 'app_login_data')
router.register(r'group_chats', GroupChatApiView, 'group_chat')






urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest-auth/login/', login_user),
    path('rest-auth/registration/', register_user),
    path('rest-auth/', include('rest_auth.urls')),
    path('account/', include('allauth.urls')),
    url(r'^rest-auth/registration/verify-email/(?P<key>.+)/$', ConfirmEmailView, name='account_confirm_email'),
    path('get_user/', get_user),
    path('rest-auth/logout/', include('rest_auth.registration.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('', include('quantumforum.urls', namespace='quantumforum')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# python manage.py dumpdata > /Users/matthewcrook/code/nss/frontEnd/quantumapp/quantumapi/fixtures/datadump.json
