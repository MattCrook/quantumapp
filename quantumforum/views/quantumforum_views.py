from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages
from quantumapi.models import UserProfile as UserProfileModel
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN, REACT_APP_FORUM_URL, REACT_APP_HOME
from django.contrib.auth import authenticate, get_backends
# from social_django.context_processors import backends
from django.contrib.auth import get_user_model

from rest_auth.models import TokenModel
# from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse

from social_django.utils import psa
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)


from social_django.context_processors import backends, user_backends_data

from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from social_core.pipeline.user import user_details
from social_core.utils import get_strategy, module_member


import datetime
import json
import jwt
import requests
import os

from social_core.actions import user_is_authenticated

# redirect_field_name = GROUP_CHAT_REDIRECT_FIELD_NAME
# success_url_allowed_hosts = []



def index(request, chat_type=None):
    print("IN Index")
    user = request.user
    # is_authenticated = user_is_authenticated(user)
    chat_type = 'group_chat'
    context = {
        'CLIENT_URL': REACT_APP_FORUM_URL,
        'user': user,
    }
    if user.is_authenticated:
        if chat_type == 'group_chat':
            return redirect(reverse('quantumforum:group_chat'))
        elif chat_type == 'private_chat':
            return redirect(private_chat)
    else:
        return redirect(reverse('quantumforum:login'))



@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def group_chat(request):
    if request.method == 'GET':
        user = request.user
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        decoded_session_data = request.session.decode(session.session_data)
        UserModel = get_user_model()
        backend_list = get_backends()
        auth_user_backends = backends(request)

        user_profile = UserProfileModel.objects.get(user_id=user.id)
        all_users = UserModel.objects.all()
        default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

        # Each join, get all that user has sent, and then all they received.
        sent_friendships = Friendships.objects.filter(requester_id=user.id)
        received_friendships = Friendships.objects.filter(addressee=user.id)
        accepted_sent_friendships = []
        accepted_sent_friend_requests = []
        accepted_received_friendships = []
        accepted_received_friend_requests = []
        quantum_friends = []
        active_friends = []
        group_chats = []

        # loop thru each join and get the friend request object.
        for f in sent_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_sent_friendships.append(f)
                    accepted_sent_friend_requests.append(friend_request)
                    addressee = UserModel.objects.get(pk=f.addressee_id)
                    quantum_friends.append(addressee)

        for f in received_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_received_friendships.append(f)
                    accepted_received_friend_requests.append(friend_request)
                    requester = UserModel.objects.get(pk=f.requester_id)
                    quantum_friends.append(requester)

        for friend in quantum_friends:
            if friend.is_active == True:
                active_friends.append(friend)

        has_active_friends = len(active_friends) > 0

        user_assoc_group_chats = GroupMembersJoin.objects.filter(user_profile_id=user_profile.id)

        for group in user_assoc_group_chats:
            group_id = group.group_id
            group_chat = GroupChat.objects.get(pk=group_id)
            group_chats.append(group_chat)


        friend_data = {
            'accepted_sent_friendships': accepted_sent_friendships,
            'accepted_sent_friend_requests': accepted_sent_friend_requests,
            'accepted_received_friendships': accepted_received_friendships,
            'accepted_received_friend_requests': accepted_received_friend_requests,
            'active_friends': active_friends
        }

        template = 'group_chat/group_chat.html'
        context = {
            'user': user,
            'user_profile': user_profile,
            'all_users': all_users,
            'friend_data': friend_data,
            'quantum_friends': quantum_friends,
            'default_profile_pic': default_profile_pic,
            'has_active_friends': has_active_friends,
            'active_friends': active_friends,
            'group_chats': group_chats,
        }
        return render(request, template, context)

    if request.method == 'POST':
        try:
            form_data = request.POST
            group_name = request.POST.get('group_name')
            all_users_in_group = set()
            user = request.user
            user_profile = UserProfileModel.objects.get(user_id=user.id)
            participant_ids = []

            for p in form_data:
                if p.split("-")[0] == 'participant':
                    participant_ids.append(p.split("-")[1])

            for pid in participant_ids:
                group_member_user_profile = UserProfileModel.objects.get(pk=pid)
                all_users_in_group.add(group_member_user_profile)

            all_group_members = list(all_users_in_group)
            all_group_members.append(user_profile)

            new_group = GroupChat()
            new_group.name = group_name
            new_group.members = all_group_members
            new_group.created_by = user
            new_group.created_at = datetime.datetime.now()
            # new_group.is_valid()
            new_group.save()


            # Then loop through all of invited group members,
            # User who created group should be included in the array.
            for member in all_group_members:
                new_group_members_join = GroupMembersJoin()
                new_group_members_join.user_profile = member
                new_group_members_join.group = new_group
                new_group_members_join.save()

        except Exception as ex:
            HttpResponse(ex.args, content='application/json')

        return redirect(reverse('quantumforum:staging_room', kwargs={'group_id': new_group.id}))



@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def staging_room(request, group_id):
    if request.method == 'GET':
        auth_user = request.user
        user_profile = UserProfileModel.objects.get(user_id=auth_user.id)
        group = GroupChat.objects.get(pk=group_id)
        group_members_join = group.group_members
        group_participants = GroupMembersJoin.objects.filter(group_id=group_id)
        group_members = set()

        for member in group_participants:
            member_user_profile = UserProfileModel.objects.get(pk=member.user_profile_id)
            group_members.add(member_user_profile)

        group_members = list(group_members)
        template = 'group_chat/staging_room.html'
        context = {
            'group': group,
            'group_members_join': group_members_join,
            'group_members': group_members,
            'auth_user': auth_user,
            'user_profile': user_profile
        }

        return render(request, template, context)




@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def private_chat(request):
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




@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def room(request, room_name):
    backends = get_backends()

    auth = request.COOKIES
    if auth and auth['auth0.is.authenticated'] == 'true':
        # user = backends[1].do_auth(token, ajax=True)
        # login(request, user)
        template = 'general/general.html'
        room_name = 'general'
        context = {
            'room_name': room_name
        }
        return render(request, template, context)



def error(request):
    template = 'errors/error.html'
    error = 'Oops! Something went wrong.'
    context = {
            'error': error,
        }
    return render(request, template, context)



# def get_user(uid):
#     token = TokenModel.objects.get(user_id=uid)
#     userdict = {
#         "first": token.user.first_name,
#         "last": token.user.last_name,
#         "email": token.user.email,
#         "username": token.user.username,
#         'auth0_identifier': token.user.auth0_identifier,
#         "is_staff": token.user.is_staff,
#         "is_superuser": token.user.is_superuser,
#         "token": token
#     }
#     return userdict


# def room(request, room_name):
#     if room_name == 'private_message':
#         if request.COOKIES and request.COOKIES['session']:
#             messages = Messages.objects.all()
#             template = 'private_message/private_message.html'
#             context = {
#                 'room_name': room_name,
#                 'messages': messages,
#             }
#         if room_name == 'general':
#             template = 'general/general.html'
#     else:
#         template = 'errors/error.html'
#         error = 'Oops! Something went wrong.'
#         context = {
#             'error': error,
#         }
#     return render(request, template, context)






# @psa('social:complete')
# def ajax_auth(request, backend):
#     """AJAX authentication endpoint"""
#     if isinstance(request.backend, BaseOAuth1):
#         token = {
#             'oauth_token': request.REQUEST.get('access_token'),
#             'oauth_token_secret': request.REQUEST.get('access_token_secret'),
#         }
#     elif isinstance(request.backend, BaseOAuth2):
#         token = request.REQUEST.get('access_token')
#     else:
#         raise HttpResponseBadRequest('Wrong backend type')
#     user = request.backend.do_auth(token, ajax=True)
#     login(request, user)
#     data = {'id': user.id, 'username': user.username}
#     return HttpResponse(json.dumps(data), mimetype='application/json')




# def authenticate_for_group_chat(request, auth_user_id):
#     UserModel = get_user_model()
#     user = UserModel.objects.get(pk=auth_user_id)
#     backend_list = get_backends()
#     cookies = request.COOKIES

#     remote_user_backend = backend_list[1]
#     model_backend = backend_list[0]
#     remote_user = remote_user_backend.get_user(auth_user_id)
#     # Use the remote user authenticate to auth wih Auth0...Auth0 backend?
#     can_authenticate = remote_user_backend.user_can_authenticate(remote_user)

#     if can_authenticate is not False:
#         secret = remote_user.auth0_identifier.split(".")[1]
#         username = remote_user.auth0_identifier

#         authenticated_user = authenticate(request, username=username, password=secret)
#         # authenticated_user = authenticate(remote_user=remote_user)
#         if authenticated_user is not None:
#             login(request, authenticated_user)
#             return HttpResponseRedirect(get_success_url(request))

#         else:
#             # Return error page and Login page if auth doesn't work.
#             template = 'errors/error.html'
#             error = 'Oops! Something went wrong.'
#             context = {
#                 'error': error,
#                 'CLIENT_URL': REACT_APP_FORUM_URL,
#                 'user': user,
#             }
#             return render(request, template, context)

#     else:
#         return redirect(reverse('quantumforum:login'))

# def get_success_url(request):
#     url = get_redirect_url(request)
#     return url or resolve_url(FORUM_LOGIN_REDIRECT_URL)

# def get_redirect_url(request):
#     """Return the user-originating redirect URL if it's safe."""
#     redirect_to = GROUP_CHAT_REDIRECT_FIELD_NAME
#     url_is_safe = url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=get_success_url_allowed_hosts(request))
#     return redirect_to if url_is_safe else ''

# def get_success_url_allowed_hosts(request):
#     return [request.get_host(), *success_url_allowed_hosts]
