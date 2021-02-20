from django.contrib import admin
from quantumapi.models import UserProfile, RollerCoaster, Tracktype, Manufacturer, Park, Credit, Messages, Image, User, NewsArticle, BlogContributorApplication, LoginHistory, ActivityLog, CalendarEvent, ErrorLog, Feedback, BugReport
from quantumapi.models import Credential as CredentialModel
from quantumapi.models import QuantumUserAdmin
from quantumapi.models import AppLoginData as AppLoginDataModel
from django.contrib.sessions.models import Session
from quantumforum.models import *
# from quantumapi.models.user_social_auth import CustomDjangoStorage
# from rest_auth.models import TokenModel
# admin.site.register(TokenModel)
# To register the join tables, have to have a custom admin, bc many to many do not have _meta.


admin.site.register(UserProfile)
admin.site.register(Tracktype)
admin.site.register(Manufacturer)
admin.site.register(Park)
admin.site.register(RollerCoaster)
admin.site.register(Credit)
admin.site.register(Messages)
admin.site.register(Image)
admin.site.register(User, QuantumUserAdmin)
admin.site.register(CredentialModel)
admin.site.register(NewsArticle)
admin.site.register(BlogContributorApplication)
admin.site.register(Session)
admin.site.register(LoginHistory)
admin.site.register(ActivityLog)
admin.site.register(CalendarEvent)
admin.site.register(ErrorLog)
admin.site.register(Feedback)
admin.site.register(BugReport)
admin.site.register(FriendRequest)
admin.site.register(StatusCode)
admin.site.register(Friendships)
admin.site.register(GroupChat)
admin.site.register(AppLoginDataModel)
admin.site.register(UsersFriends)
