# from rest_framework import routers
# from django.conf.urls import include
# from django.urls import path
# from quantumapi.views import RollerCoasters, Manufacturers, Parks, Tracktypes, UserProfiles, Message, Credits, Users, Images, News, BlogContributorApplications, ActivityLogView, LoginInfoView, CalendarEvents, ErrorLogView
# from quantumapi.views import login_user, register_user, get_user, auth0_logout
# from quantumapi.views import Credentials as CredentialsView


# router = routers.DefaultRouter(trailing_slash=False)

# router.register(r'parks', Parks, 'park')
# router.register(r'tracktypes', Tracktypes, 'tracktype')
# router.register(r'manufacturers', Manufacturers, 'manufacturer')
# router.register(r'rollercoasters', RollerCoasters, 'rollercoaster')
# router.register(r'userprofiles', UserProfiles, 'userprofile')
# router.register(r'credits', Credits, 'credit')
# router.register(r'messages', Message, 'messages')
# router.register(r'users', Users, 'user')
# router.register(r'images', Images, 'image')
# router.register(r'credentials', CredentialsView, 'credentials')
# router.register(r'news', News, 'news')
# router.register(r'contributor_applications', BlogContributorApplications, 'contributor_application')
# router.register(r'activity_log', ActivityLogView, 'activity_log')
# router.register(r'login_info', LoginInfoView, 'login_info')
# router.register(r'calendar_events', CalendarEvents, 'calendar_event')
# router.register(r'error_logs', ErrorLogView, 'error_logs')


# urlpatterns = [
#     path('api/', include(router.urls)),
# ]
