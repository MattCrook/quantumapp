from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages, User, UserProfile
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN, REACT_APP_FORUM_URL
from django.contrib.auth import authenticate, get_backends
from social_django.context_processors import backends

import json
import jwt
import requests
import os

def index(request):
    template = 'forum/index.html'
    context = {}
    return render(request, template, context)

def group_chat(request, auth_user_id):
    backend = get_backends()
    backends_context = backends(request)
    user_profile = UserProfile.objects.get(user_id=auth_user_id)
    all_users = User.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    template = 'group_chat/group_chat.html'
    context = {
        'user_profile': user_profile,
        'all_users': all_users,
        'CLIENT_URL': REACT_APP_FORUM_URL
    }
    return render(request, template, context)


def private_chat(request, auth_user_id):
    backend = get_backends()
    backends_context = backends(request)

    user_profile = UserProfile.objects.get(user_id=auth_user_id)
    all_users = User.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    template = 'private_message/private_message.html'
    context = {
        'user_profile': user_profile,
        'all_users': all_users,
        'CLIENT_URL': REACT_APP_FORUM_URL
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




# @login_required
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
