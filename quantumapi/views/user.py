import json
from rest_framework.response import Response
from rest_framework import viewsets, status, serializers
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseServerError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.serializers import ModelSerializer
from ..models import User, UserProfile, ImageForm

# from rest_auth.models import DefaultTokenModel
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        user = serializers.SerializerMethodField()
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username',
                  'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'auth0_identifier', 'is_superuser', 'is_active',  )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class Users(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']


    @csrf_exempt
    def get_user(self, request):

        req_body = json.loads(request.body.decode())
        if request.method == 'POST':
            # Use the built-in authenticate method to verify
            token = req_body['token']
            user = DefaultTokenModel.objects.get(key=token).user
            userdict = {
                "first": user.first_name,
                "last": user.last_name,
                "email": user.email,
                "username": user.username,
                'auth0_identifier': auth0_identifier,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "token": token
            }
            return HttpResponse(json.dumps(userdict), content_type='application/json')
