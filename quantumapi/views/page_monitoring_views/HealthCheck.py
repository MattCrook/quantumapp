from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from dataclasses import dataclass
import json


class HealthCheck(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        try:
            health = {
                'status': 'successful',
            }
            return HttpResponse(json.dumps(health), content_type='application/json')
        except Exception as ex:
            error = {
                'error': ex,
                'status': 'unsuccessful'
            }
            return HttpResponseServerError(json.dumps(error), content_type='application/json')
