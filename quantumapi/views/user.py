from rest_framework.response import Response
from rest_framework import viewsets, status, serializers
from rest_framework.serializers import ModelSerializer
from django.http import HttpResponseServerError, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from ..models import UserProfile, ImageForm
from rest_auth.models import TokenModel
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.sessions.models import Session
import json





class UserSerializer(serializers.ModelSerializer):
    # def get_queryset(self):
    #     return super().get_queryset()
    
    class Meta:
        model = get_user_model()
        # token = serializers.SerializerMethodField()
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username',
                  'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'auth0_identifier', 'is_superuser', 'is_active',  )
        # extra_kwargs = {'password': {'write_only': True}}
        depth = 2


class Users(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        UserModel = get_user_model()
        try:
            users = UserModel.objects.all()
            email = self.request.query_params.get('email', None)

            if email is not None:
                users = UserModel.objects.filter(email=email)

            serializer = UserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        UserModel = get_user_model()
        try:
            user = UserProfile.objects.get(pk=pk)
            email = self.request.query_params.get('email', None)

            if email is not None:
                user = UserModel.objects.filter(email=email)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=pk)
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.email = request.data['email']
            user.username = request.data['username']

            if 'auth0_identifier' in request.data:
                user.auth0_identifier = request.data['auth0_identifier']

            if 'is_superuser' in request.data:
                user.is_superuser = request.data['is_superuser']

            user.save()
            return Response({'UserProfile Updated Successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=pk)
            user.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def get_user_session(request):
    if request.method == 'POST':
        req_body = json.loads(request.body.decode())
        token = request.auth
        auth_user_token = TokenModel.objects.get(key=token.key)
        if auth_user_token.user_id == request.user.id:
            auth_user = request.user
            session = request.session
            decoded_session_data = session.get_decoded()
            auth_session_hash_data = auth_user.get_session_data(session)

            data = {
                'decoded_session_data': decoded_session_data,
                'auth_hash_data': auth_session_hash_data,
                'token': auth_user_token.key
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = json.dumps({"valid": False, "Error": 'Missing or incorrectly matching authentication.'})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'GET':
        try:
            auth_user = request.user
            session_key = request.session.session_key
            session = Session.objects.get(session_key=session_key)
            session_store_class = session.get_session_store_class()
            decoded_session_data = session.get_decoded()
            auth_user_token = TokenModel.objects.get(user_id=auth_user.id)
            auth_session_hash_data = auth_user.get_session_data(session)

            data = {
                'decoded_session_data': decoded_session_data,
                'auth_hash_data': auth_session_hash_data,
                'token': auth_user_token.key
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as ex:
            return Response({'error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# def get_auth_user(self, obj):
#     serialized_user = UserSerializer(instance=obj.auth_user)
#     return serialized_user.data

# @authentication_classes([SessionAuthentication, JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view
# def get_authuser(self, request):
#     # req_body = json.loads(request.body.decode())
#     if request.method == 'POST':
#         user = request.user
#         session = request.session
#         decoded_session_data = session.decode(session.session_data)
#         # token = req_body['token']
#         token = TokenModel.objects.get(user_id=user.id)
#         userdict = {
#             "first": user.first_name,
#             "last": user.last_name,
#             "email": user.email,
#             "username": user.username,
#             'auth0_identifier': user.auth0_identifier,
#             "is_staff": user.is_staff,
#             "is_superuser": user.is_superuser,
#             "token": token.key,
#             'session_data': decoded_session_data
#         }
#         return HttpResponse(json.dumps(userdict), content_type='application/json')




# class Users(viewsets.ModelViewSet):
    # queryset = UserModel.objects.all()
    # print("QUERYSET", queryset)
    # serializer_class = UserSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['email']
