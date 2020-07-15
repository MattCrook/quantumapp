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

        # If image_id is not none meaning there is an image this is an edit where there is already a photo
        if userprofile.image_id is not None:
            image_id = userprofile.image_id
            image = Image.objects.get(pk=image_id)
            image.image = request.FILES["image"]
            image.save()

            userprofile.address = request.data["address"]
            userprofile.image_id = image.id
            userprofile.user_id = userprofile_user_id

        else:
            userprofile.address = request.data["address"]
            new_image = Image()
            new_image.image = request.FILES["image"]
            new_image.save()

            userprofile.image_id = new_image.id
            userprofile.user_id = userprofile_user_id
            userprofile.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Checking url if email is passed in then we are looking at the auth user resource
        # if email is not None:

        # user.first_name = request.data["first_name"]
        # user.last_name = request.data["last_name"]
        # user.username = request.data["username"]
        # user.save()

        # image.image = request.FILES["image"]
        # image.save()
        # image = ImageForm(request.POST, request.FILES)

        # userprofile.image = image.id
        # userprofile.user = user
        # userprofile.image_id = image_id

        # image.image = request.data["picUrl"]

        # return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            userprofile.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # elif request.method == 'POST':
        #     form_data = request.POST
        #     if ('actual_method' in form_data and form_data['actual_method'] == 'PUT'):
        #         userprofile = UserProfile.objects.get(pk=pk)
        #         userprofile_user_id = userprofile.user_id
        #         image_id = userprofile.image_id
        #         user = User.objects.get(pk=userprofile_user_id)
        #         email = self.request.query_params.get('email', None)

        #         # if request.FILES:
        #         #     userprofile.image_path = request.FILES["image_path"]
        #         image = ImageForm(request.POST, request.FILES)
        #         user.first_name = form_data["first_name"]
        #         user.last_name = form_data["last_name"]
        #         user.username = form_data["username"]
        #         userprofile.address = form_data["address"]
        #         image.save()

        #         img_obj = image.instance
        #         img_obj.image = request.FILES["image"]
        #         image.save()

        #         userprofile.image_id = img_obj.id
        #         user.save()
        #         userprofile.save()

        #     return Response({}, status=status.HTTP_204_NO_CONTENT)

        # If we have an image(profile pic)
        # if userprofile.image_id is not None:
        #     image_id = userprofile.image_id
        #     image = Image.objects.get(pk=image_id)
        #     user = User.objects.get(pk=user_id)

        #     userprofile.address = request.data["address"]
        #     userprofile.image_id = image_id
        #     userprofile.save()

        #     image.image = request.data["picUrl"]
        #     image.save()

        #     if email is not None:
        #         user.first_name = request.data["first_name"]
        #         user.last_name = request.data["last_name"]
        #         user.username = request.data["username"]
        #         user.save()
        # else:
        #     user = User.objects.get(pk=user_id)
        #     print("ELSE")

            # image = ImageForm(request.POST, request.FILES)
            # image.save()

            # img_obj = image.instance
            # img_obj.image = request.FILES["image"]
            # image.save()

            # userprofile.image_id = img_obj.id
            # user.save()
            # userprofile.save()

            ###########
            # image = Image()
            # image.image = request.data["picUrl"]
            # image.save()

            # userprofile.address = request.data["address"]
            # userprofile.image = image.id
            # userprofile.user_id = user.id
            # userprofile.save()

            # if email is not None:
            #     print("IFEMAIL")
            #     user.first_name = request.data["first_name"]
            #     user.last_name = request.data["last_name"]
            #     user.username = request.data["username"]
            #     user.save()

        # # saving userprofile should also save and update the User table.
        # # Find on UserProfile models. They are linked together.
        # return Response({}, status=status.HTTP_204_NO_CONTENT)
