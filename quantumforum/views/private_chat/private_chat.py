from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages
from quantumapi.models import UserProfile as UserProfileModel
from django.contrib.sessions.models import Session
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_backends
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from quantumapp.settings import REACT_APP_FORUM_URL
import datetime




@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def private_chat_view(request):
    UserModel = get_user_model()
    backend_list = get_backends()
    auth_user = request.user

    user_profile = UserProfileModel.objects.get(user_id=auth_user.id)
    all_users = UserModel.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    template = 'private_message/private_message.html'
    context = {
        'user_profile': user_profile,
        'all_users': all_users,
        'CLIENT_URL': REACT_APP_FORUM_URL
    }
    return render(request, template, context)
