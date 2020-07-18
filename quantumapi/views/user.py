import json
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseServerError
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from quantumapi.permissions import IsLoggedIUserOrAdmin, IsAdminUser
# from rest_framework.views import APIView
from quantumapi.auth0_views import get_token_auth_header, requires_scope
from django.http import HttpResponseServerError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from quantumapi.models.model_factory import model_factory
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from quantumapi.models import User, UserProfile, ImageForm
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from quantumapi.auth0_views import requires_scope
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        email = serializers.SerializerMethodField()
        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'password', 'username',
                  'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class Users(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedIUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsLoggedIUserOrAdmin]
    #     return [permission() for permission in permission_classes]


    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # @csrf_exempt
    def create(self, request):
        try:
            req_body = json.loads(request.body.decode())

            new_user = User.objects.create_user(
                username=req_body['username'],
                email=req_body['email'],
                password=req_body['password'],
                first_name=req_body['first_name'],
                last_name=req_body['last_name']
            )
            new_userprofile = UserProfile.objects.create(
                address=req_body["address"],
                user=new_user
            )
            new_userprofile.save()
            # token = Token.objects.create(user=new_user)
            # key = token.key

            # Specifying the response that the API sends back From making a POST to Users. (the .then() from client side.)
            userdict = {
                "first": new_user.first_name,
                "last": new_user.last_name,
                "email": new_user.email,
                "username": new_user.username,
                "is_staff": new_user.is_staff
                # "token": key
            }
            data = json.dumps({"QuantumUserData": userdict})
            return HttpResponse(data, content_type='application/json')
        except Exception as x:
            return HttpResponse(x, content_type='application/json')

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)

        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.username = request.data["username"]
        user.email = request.data["email"]

        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

@csrf_exempt
def get_user(request):

    req_body = json.loads(request.body.decode())
    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        token = req_body['token']
        user = Token.objects.get(key=token).user
        userdict = {
            "first": user.first_name,
            "last": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "token": token
        }
        return HttpResponse(json.dumps(userdict), content_type='application/json')



# def create(self, validated_data):
        #     print(validated_data)
        #     # password was .pop()...need the password for the DB...was loosing it at registration.
        #     password = validated_data.pop('password')
        #     user = User(**validated_data)
        #     user.email = validated_data.get('email')
        #     user.set_password(password)
        #     user.save()
        #     print("USER", user)
        #     return user
