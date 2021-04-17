# from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from dataclasses import dataclass
import json




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, SessionAuthentication])
def health_check(request):
    if request.method == 'GET':
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
