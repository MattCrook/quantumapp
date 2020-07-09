import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import UserProfile, Credit, Image
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth.models import User
from .user import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        url = serializers.HyperlinkedIdentityField(
            view_name='userprofile',
            lookup_field='id'
        )
        fields = ('id', 'address', 'image', 'credits', 'user', )
        depth = 1
        # extra_kwargs = {'password': {'write_only': True}}


class UserProfiles(ViewSet):
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.TokenAuthentication]

    def list(self, request):
        try:
            userprofiles = UserProfile.objects.all()
            email = self.request.query_params.get('email', None)
            if email is not None:
                auth_user = User.objects.filter(email=email)
                serializer = UserSerializer(auth_user, many=True, context={'request': request})
            else:
                serializer = UserProfileSerializer(userprofiles, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        userprofile = UserProfile.objects.get(pk=pk)
        user_id = userprofile.user_id
        image_id = userprofile.image_id

        image = Image.objects.get(pk=image_id)
        user = User.objects.get(pk=user_id)

        userprofile.address = request.data["address"]
        userprofile.save()

        image.image = request.data["picUrl"]
        image.save()

        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.username = request.data["username"]
        user.save()

        # # saving userprofile should also save and update the User table.
        # # Find on UserProfile models. They are linked together.
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
