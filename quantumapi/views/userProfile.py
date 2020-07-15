import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import UserProfile, Credit, Image, User
# from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# from django.contrib.auth import login, authenticate
from django.conf import settings
from .user import UserSerializer
# from quantumapi.models import ImageForm


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        url = serializers.HyperlinkedIdentityField(
            view_name='userprofile',
            lookup_field='id'
        )
        fields = ('id', 'address', 'image', 'credits', 'user', )
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}


class UserProfiles(ViewSet):
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.TokenAuthentication]

    def list(self, request):
        try:
            userprofiles = UserProfile.objects.all()
            email = self.request.query_params.get('email', None)
            user_id = self.request.query_params.get('userId', None)

            if email is not None:
                auth_user = User.objects.filter(email=email)
                serializer = UserSerializer(
                    auth_user, many=True, context={'request': request})
            elif user_id is not None:
                userprofile = UserProfile.objects.filter(user_id=user_id)
                serializer = UserProfileSerializer(
                    userprofile, many=True, context={'request': request})
            else:
                serializer = UserProfileSerializer(
                    userprofiles, many=True, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(
                userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        userprofile = UserProfile.objects.get(pk=pk)
        userprofile_user_id = userprofile.user_id
        user = User.objects.get(pk=userprofile_user_id)
        email = self.request.query_params.get('email', None)

        userprofile.address = request.data["address"]
        userprofile.image_id = request.data["image_id"]
        userprofile.save()


        # If image_id is not none meaning there is an image this is an edit where there is already a photo
        # if userprofile.image_id is not None:
        #     image_id = userprofile.image_id
        #     image = Image.objects.get(pk=image_id)
        #     image.image = request.FILES["image_id"]
        #     image.save()

        #     userprofile.address = request.data["address"]
        #     userprofile.image_id = request.data["image_id"]
        #     userprofile.user_id = userprofile_user_id
        #     userprofile.save()
        #     print("userprofileISNOTNONE", userprofile)

        # elif userprofile.image_id is None:
        #     userprofile.address = request.data["address"]
        #     new_image = Image()
        #     new_image.image = request.FILES["image"]
        #     new_image.save()

        #     userprofile.image_id = new_image.id
        #     userprofile.user_id = userprofile_user_id
        #     userprofile.save()
        #     print("userprofileNONE", userprofile)


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
