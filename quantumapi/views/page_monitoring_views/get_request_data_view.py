from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from social_django.context_processors import backends, user_backends_data
import json



def get_request_data(request):
    user = request.user
    session = request.session
    backends = backends(request)
    successful_authenticator = request.successfull_authenticator

    req_data = {}



    data = json.dumps(req_data)
    return HttpResponse(data, content_type='application/json')
