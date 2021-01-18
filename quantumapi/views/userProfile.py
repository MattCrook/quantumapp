from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from .user import UserSerializer
from quantumapi.models import UserProfile, Credit, Image, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import login, authenticate
# from quantumapi.models import ImageForm
# from quantumapi.auth0_views import requires_scope


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        url = serializers.HyperlinkedIdentityField(view_name='userprofile', lookup_field='id')
        fields = ('id', 'address', 'image', 'credits', 'user', )
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}


class UserProfiles(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]


    def list(self, request):
        try:
            userprofiles = UserProfile.objects.all()
            serializer = UserProfileSerializer(userprofiles, many=True, context={'request': request})
            email = self.request.query_params.get('email', None)
            user_id = self.request.query_params.get('userId', None)

            if email is not None:
                auth_user_data = User.objects.get(email=email)
                userprofiles = UserProfile.objects.get(user_id=auth_user_data.id)
                serializer = UserProfileSerializer(userprofiles, context={'request': request})

            elif user_id is not None:
                userprofiles = UserProfile.objects.get(user_id=user_id)
                serializer = UserProfileSerializer(userprofiles, context={'request': request})

            return Response(serializer.data)

        except:
            if UserProfile.DoesNotExist:
                return HttpResponse({"Error": "No User matching query."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': Exception.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile_user_id = userprofile.user_id
            user = User.objects.get(pk=userprofile_user_id)
            email = self.request.query_params.get('email', None)

            if 'image' in request.data and request.data['image']:
                new_image = request.data['image']
                image = Image.objects.get(pk=new_image['id'])
                userprofile.image = image

            userprofile.address = request.data["address"]
            userprofile.user = user

            userprofile.save()
            return Response({'UserProfile Updated Successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
