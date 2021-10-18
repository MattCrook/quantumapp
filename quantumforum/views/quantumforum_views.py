from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required, permission_required
from quantumapi.models import Credential, Messages
from quantumapi.models import UserProfile as UserProfileModel
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN, CLIENT_URL, REACT_APP_FORUM_URL, REACT_APP_HOME
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

# from httplib2 import Http
from social_django.models import DjangoStorage


import datetime
import json
import jwt
import requests
import os

from social_core.actions import user_is_authenticated

# redirect_field_name = GROUP_CHAT_REDIRECT_FIELD_NAME
# success_url_allowed_hosts = []


# @permission_required([IsAuthenticated])
# @login_required
def index(request, chat_type=None):
    print("IN Index")
    user = request.user
    is_auth = request.user.is_authenticated
    is_remote_authenticated = user_is_authenticated(user)
    if is_auth:

        if user and hasattr(user, 'social_auth'):
            is_social_auth = user.social_auth.filter(user_id=user.id).exists()
            if is_social_auth:
                social_user = user.social_auth.get(user_id=user.id)
                provider = social_user.provider
                if provider == 'auth0':
                    auth0user = user.social_auth.get(provider='auth0')
                    userdata = {
                        'user_id': auth0user.uid,
                        'name': user.first_name,
                        'picture': auth0user.extra_data['picture'],
                        'email': auth0user.extra_data['email'],
                        'token': auth0user.extra_data['access_token']
                    }
                    user_id = auth0user.user_id
                    chat_type = 'group_chat'
                    context = {
                        'CLIENT_URL': REACT_APP_FORUM_URL,
                        'user': user,
                        'auth0User': auth0user,
                        'userdata': json.dumps(userdata, indent=4),
                    }

                    if chat_type == 'group_chat':
                        return redirect(reverse('quantumforum:group_chat'))
                    elif chat_type == 'private_chat':
                        return redirect(private_chat)

            # elif provider == 'google-oauth2':
            #     UserModel = get_user_model()
            #     auth_user = UserModel.objects.get(username=user)
            #     user_id = auth_user.id
            #     status = True

            #     if not request.user.is_authenticated:
            #         return HttpResponseRedirect('login')

            #     storage = DjangoStorage(CredentialsModel, 'user_id', request.user, 'credential')
            #     credential = storage.get()
            #     try:
            #         access_token = credential.access_token
            #         resp, cont = Http().request("https://www.googleapis.com/auth/gmail.readonly",
            #                                     headers={'Host': 'www.googleapis.com',
            #                                             'Authorization': access_token})
            #     except:
            #         status = False
            #         print('Not Found')

            #     template = 'home/home.html'
            #     context = {
            #         'user': user_data,
            #         'admin_user': admin_user,
            #         'status': status,
            #         'credential': credential
            #     }
            #     return render(request, template, context)

            # chat_type = 'group_chat'
            # context = {
            #     'CLIENT_URL': REACT_APP_FORUM_URL,
            #     'user': user,
            # }


    else:
        return redirect(reverse('quantumforum:login'))



@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
@permission_required([IsAuthenticated])
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
            'CLIENT_URL': CLIENT_URL
        }
    return render(request, template, context)




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
