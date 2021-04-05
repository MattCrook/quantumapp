from quantumapi.views.auth.management_api_services import management_api_oath_endpoint, get_management_api_user, get_open_id_config, management_api_openid_authorization_codes
from quantumapp import settings
from quantumadminapp.views import index

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import login, admin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import error, success, INFO
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseBadRequest

import json
from django.contrib.auth import get_backends
from social_core.actions import user_is_authenticated, do_auth

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
# from rest_framework.decorators import renderer_classes
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from rest_framework.authentication import TokenAuthentication



def login_admin_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body.decode())
            email = req_body['email']
            password = req_body['password']
            UserModel = get_user_model()
            backends = get_backends()
            # openid_backend = backends[0]
            admin_user = UserModel.objects.get(email=email['email'])
            authenticated_user = authenticate(request, auth0_identifier=admin_user.auth0_identifier, password=password['password'], backend=backends[4])
            is_user_authenticated = user_is_authenticated(authenticated_user)
            if authenticated_user is not None and is_user_authenticated:
                token = Token.objects.get(user=authenticated_user)
                # openid_authorize = openid_connect_authorize_endpoint(settings.AUTH0_DOMAIN)
                management_api_oauth_endpoint_result = management_api_oath_endpoint(settings.AUTH0_DOMAIN)
                management_api_token = json.loads(management_api_oauth_endpoint_result)
                management_api_jwt = management_api_token['access_token']
                management_api_admin_user = get_management_api_user(settings.AUTH0_DOMAIN, management_api_jwt, authenticated_user.auth0_identifier.replace(".", "|"))
                openid_endpoint = get_open_id_config(settings.AUTH0_DOMAIN, management_api_jwt)
                login(request, authenticated_user, backend='quantumapi.auth0_backend.QuantumAdminOpenID')

                data = {
                    "valid": True,
                    "token": token.key,
                    "first_name": authenticated_user.first_name,
                    "last_name": authenticated_user.last_name,
                    "email": authenticated_user.email,
                    "username": authenticated_user.username,
                    "auth0_identifier": authenticated_user.auth0_identifier,
                    "management_api_token": management_api_token,
                    "management_jwt": management_api_jwt,
                    "id_token": management_api_jwt,
                    "management_user": management_api_admin_user,
                    # "last_login": authenticated_user.last_login,
                    "is_superuser": authenticated_user.is_superuser,
                    "is_staff": authenticated_user.is_staff,
                     }
                data = json.dumps(data)
                return HttpResponse(data, content_type='application/json')
            else:
                data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
        #     print('IN GET')
        #     # A GET on page refresh. Either do a error page, or get this form page, or get redirect to index again to let react route it.
            # return redirect('/quantumadmin/admin_login/')
    except Exception as ex:
        return HttpResponse(ex.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_and_forward_to_login(request):
    try:
        csrf_token = get_token(request)
        data = {
            'csrf': csrf_token
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception as ex:
        data = json.dumps({"valid": False, "Error": ex})
        return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# def django_admin_login(request):
#     admin(request)
#     return redirect(reverse('quantumadminapp:admin'))
