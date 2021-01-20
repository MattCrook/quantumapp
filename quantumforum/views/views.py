from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages, UserProfile
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN, REACT_APP_FORUM_URL, FORUM_LOGIN_REDIRECT_URL, GROUP_CHAT_REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, get_backends
# from social_django.context_processors import backends
from django.contrib.auth import get_user_model

from rest_auth.models import TokenModel
# from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.urls import reverse

# from social_django.utils import psa
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)


from social_django.context_processors import backends, user_backends_data



import json
import jwt
import requests
import os



redirect_field_name = GROUP_CHAT_REDIRECT_FIELD_NAME
success_url_allowed_hosts = set()





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
        # return render(request, 'login.html', context)
        return redirect(reverse('quantumforum:login'))



def home(request):
    pass



def authenticate_for_group_chat(request, auth_user_id):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=auth_user_id)
    backend_list = get_backends()
    remote_user_backend = backend_list[1]
    model_backend = backend_list[0]
    remote_user = remote_user_backend.get_user(auth_user_id)
    can_authenticate = remote_user_backend.user_can_authenticate(remote_user)

    if can_authenticate is not False:
        secret = user.auth0_identifier.split(".")[1]
        username = user.auth0_identifier

        authenticated_user = authenticate(request, username=username, password=secret)
        # authenticated_user = authenticate(remote_user=remote_user)
        if authenticated_user is not None:
            auth_login(request, authenticated_user, backend='django.contrib.auth.backends.RemoteUserBackend')
            return HttpResponseRedirect(get_success_url(request))
            # return redirect(reverse('quantumforum:group_chat'))
        else:
            # Return error page and Login page if auth doesnt work
            print("not authenticated")
    else:
        print("can't authenticated")




def get_success_url(request):
    url = get_redirect_url(request)
    return url or resolve_url(FORUM_LOGIN_REDIRECT_URL)

def get_redirect_url(request):
    """Return the user-originating redirect URL if it's safe."""
    redirect_to = request.POST.get(
        redirect_field_name,
        request.GET.get(redirect_field_name, '')
    )
    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=get_success_url_allowed_hosts(request),
        # require_https=request.is_secure(),
    )
    return redirect_to if url_is_safe else ''

def get_success_url_allowed_hosts(request):
    return {request.get_host(), *success_url_allowed_hosts}


# def form_valid(self, form):
    # """Security check complete. Log the user in."""
    # login(self.request, form.get_user())
    # return HttpResponseRedirect(get_success_url())


@login_required
def group_chat(request):
    user = request.user
    session = request.session
    UserModel = get_user_model()
    backend_list = get_backends()
    auth_user_backends = backends(request)

    # user = get_user(user.id)
    user_profile = UserProfile.objects.get(user_id=user.id)
    all_users = UserModel.objects.all()
    default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

    template = 'group_chat/group_chat.html'
    context = {
        'user': user,
        'user_profile': user_profile,
        'all_users': all_users
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
