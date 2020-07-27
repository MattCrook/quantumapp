import json
from rest_framework.response import Response
from rest_framework import viewsets, status, serializers
from rest_framework.serializers import ModelSerializer
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseServerError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..models import UserProfile, ImageForm
from rest_auth.utils import default_create_token
from rest_auth.serializers import TokenSerializer
from django.contrib.auth import get_user_model


# from rest_framework.authtoken.models import Token
# from quantumapp import settings
# from rest_auth.models import DefaultTokenModel
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        token = serializers.SerializerMethodField()
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username',
                  'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'auth0_identifier', 'is_superuser', 'is_active',  )
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class Users(viewsets.ModelViewSet):
    User = get_user_model()

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']



    # def get_token(self, request):
    #     if request.method == 'GET':
    #         token = default_create_token(Token, user, seTokenSerializer)

    # def list(self, request):
    #     users = settings.AUTH_USER_MODEL.objects.all()
    #     email = self.request.query_params.get('email', None)
    #     if email is not None:
    #         users = User.objects.filter(email=email)
    #     serializer = UserSerializer(users, many=True, context={'request': request})
    #     return Response(serializer.data)


    # def update(self, request, pk=None):
    #     try:
    #         user = settings.AUTH_USER_MODEL.objects.get(pk=pk)
    #         user.first_name = request.data["first_name"]
    #         user.last_name = request.data["last_name"]
    #         user.username = request.data["username"]
    #         user.password = request.data["password"]
    #         user.email = request.data["email"]
    #         user.save()
    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except settings.AUTH_USER_MODEL.DoesNotExist as ex:
    #         return Response({'DoesNotExist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as ex:
    #         return Response({'Exception': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # def destroy(self, request, pk=None):
    #     try:
    #         user = settings.AUTH_USER_MODEL.objects.get(pk=pk)
    #         user.delete()
    #         return Response({f'User {user.id} Deleted'}, status=status.HTTP_204_NO_CONTENT)

    #     except User.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@csrf_exempt
def get_user(self, request):

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
            'auth0_identifier': auth0_identifier,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "token": token
        }
        return HttpResponse(json.dumps(userdict), content_type='application/json')
