from quantumapi.views.auth.management_api_services import management_api_oath_endpoint
from quantumapp import settings

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status


from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth import login, admin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import error, success, INFO
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseBadRequest
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_django.utils import psa
import json



# def admin_user(request):
#     admin(request)
#     return redirect()


@csrf_exempt
def login_admin_user(request):
    try:
        req_body = json.loads(request.body.decode())
        if request.method == 'POST':
            email = req_body['email']
            password = req_body['password']
            authenticated_user = authenticate(request, email=email, password=password)
            if authenticated_user is not None:
                token = Token.objects.get(user=authenticated_user)
                management_api_oauth_endpoint_result = management_api_oath_endpoint(settings.AUTH0_DOMAIN)
                management_api_token = json.loads(management_api_oauth_endpoint_result)
                management_api_jwt = management_api_token['access_token']
                login(request, authenticated_user)

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
                     }
                data = json.dumps(data)
                return HttpResponse(data, content_type='application/json')
            else:
                data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # A GET on page refresh. Either do a error page, or get this form page, or get redirect to index again to let react route it.
            pass

    except Exception as ex:
        return Response(ex.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
