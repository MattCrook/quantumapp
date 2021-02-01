from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages, UserProfile
from quantumforum.models import Friendships, FriendRequest
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN, REACT_APP_FORUM_URL, FORUM_LOGIN_REDIRECT_URL, GROUP_CHAT_REDIRECT_FIELD_NAME, REACT_APP_HOME
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


import json
import jwt
import requests
import os



redirect_field_name = GROUP_CHAT_REDIRECT_FIELD_NAME
success_url_allowed_hosts = []

def get_success_url(request):
    url = get_redirect_url(request)
    return url or resolve_url(FORUM_LOGIN_REDIRECT_URL)

def get_redirect_url(request):
    """Return the user-originating redirect URL if it's safe."""
    redirect_to = GROUP_CHAT_REDIRECT_FIELD_NAME
    url_is_safe = url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=get_success_url_allowed_hosts(request))
    return redirect_to if url_is_safe else ''

def get_success_url_allowed_hosts(request):
    return [request.get_host(), *success_url_allowed_hosts]




def index(request, chat_type):
    user = request.user
    context = {
        'CLIENT_URL': REACT_APP_FORUM_URL
    }
    if user.is_authenticated:
        if chat_type == 'group_chat':
            return redirect(group_chat)
        elif chat_type == 'private_chat':
            return redirect(private_chat)
    else:
        return redirect(reverse('quantumforum:login'))



def home(request):
    pass



def authenticate_for_group_chat(request, auth_user_id):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=auth_user_id)
    backend_list = get_backends()
    cookies = request.COOKIES

    remote_user_backend = backend_list[1]
    model_backend = backend_list[0]
    remote_user = remote_user_backend.get_user(auth_user_id)
    # Use the remote user authenticate to auth wih Auth0...Auth0 backend?
    can_authenticate = remote_user_backend.user_can_authenticate(remote_user)

    if can_authenticate is not False:
        secret = remote_user.auth0_identifier.split(".")[1]
        username = remote_user.auth0_identifier

        authenticated_user = authenticate(request, username=username, password=secret)
        # authenticated_user = authenticate(remote_user=remote_user)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return HttpResponseRedirect(get_success_url(request))

        else:
            # Return error page and Login page if auth doesn't work.
            template = 'errors/error.html'
            error = 'Oops! Something went wrong.'
            context = {
                'error': error,
                'CLIENT_URL': REACT_APP_FORUM_URL,
            }
            return render(request, template, context)

    else:
        return redirect(reverse('quantumforum:login'))



@login_required
def group_chat(request):
    user = request.user
    session = request.session
    UserModel = get_user_model()
    backend_list = get_backends()
    auth_user_backends = backends(request)

    user_profile = UserProfile.objects.get(user_id=user.id)
    all_users = UserModel.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    # Each join, get all that user has sent, and then all they receieved. 
    sent_friendships = Friendships.objects.filter(requester_id=user.id)
    received_friendships = Friendships.objects.filter(addressee=user.id)
    accepted_sent_friendships = []
    accepted_sent_friend_requests = []
    accepted_received_friendships = []
    accepted_received_friend_requests = []
    quantum_friends = []
    active_friends  = []



    # loop thru each join and get the friend request object.
    for f in sent_friendships:
        friendship_id = f.id
        is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
        if is_friend_request is not None:
            friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
            if friend_request.status_code.code == '1':
                accepted_sent_friendships.append(f)
                accepted_sent_friend_requests.append(friend_request)
                addressee = UserModel.objects.get(pk=f.addressee_id)
                quantum_friends.append(addressee)

    for f in received_friendships:
        friendship_id = f.id
        is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
        if is_friend_request is not None:
            friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if friend_request.status_code.code == '1':
                accepted_received_friendships.append(f)
                accepted_received_friend_requests.append(friend_request)
                requester = UserModel.objects.get(pk=f.requester_id)
                quantum_friends.append(requester)

    for friend in quantum_friends:
        if friend.is_active == True:
            active_friends.append(friend)

    has_active_friends = len(active_friends) > 0




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

    }
    return render(request, template, context)


@login_required
def private_chat(request, auth_user_id):
    UserModel = get_user_model()
    backend_list = get_backends()

    user_profile = UserProfile.objects.get(user_id=auth_user_id)
    all_users = UserModel.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    template = 'private_message/private_message.html'
    context = {
        'user_profile': user_profile,
        'all_users': all_users,
        'CLIENT_URL': REACT_APP_FORUM_URL
    }
    return render(request, template, context)





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








def get_user(uid):
    token = TokenModel.objects.get(user_id=uid)
    userdict = {
        "first": token.user.first_name,
        "last": token.user.last_name,
        "email": token.user.email,
        "username": token.user.username,
        'auth0_identifier': token.user.auth0_identifier,
        "is_staff": token.user.is_staff,
        "is_superuser": token.user.is_superuser,
        "token": token
    }
    return userdict


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
