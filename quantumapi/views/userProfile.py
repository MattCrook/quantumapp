from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import UserProfile, Credit, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.conf import settings


# from django.conf import settings


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        url = serializers.HyperlinkedIdentityField(
            view_name='userprofile',
            lookup_field='id'
        )
        fields = ('id', 'url', 'address', 'picUrl', 'credits', )
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}


class UserProfiles(ViewSet):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.TokenAuthentication]

    # @csrf_exempt
    def create(self, request):
        req_body = json.loads(request.body.decode())
        print("REQ_BODY", req_body)
        # user = settings.AUTH_USER_MODEL

        new_user = User.objects.create(
            first_name=req_body['first_name'],
            last_name=req_body['last_name'],
            username=req_body['username'],
            # password=req_body['password'],
            email=req_body['email'],
        )

        userprofile = UserProfile.objects.create(
            address=req_body['address'],
            picUrl=req_body['picUrl'],
            # credits=req_body['rollerCoaster_id'],
            user=new_user
        )

        userprofile.save()

        #calls the manager
        token = Token.objects.create(user=new_user)
        # token = Token.objects.create_userProfile(user=userprofile)

        # Return the token to the client
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')


    # def create(self, request):
    #     # user = User.objects.get(user=request.auth.user)
    #     user = User.objects.create_user(user=request.auth.user)

    #     first_name = user["first_name"]
    #     last_name = user["last_name"]
    #     username = user["username"]
    #     email = user["email"]
    #     rollerCoaster_id = Credit.objects.get(pk="credits")

    #     newuserprofile = UserProfile()
    #     newuserprofile.first_name = first_name
    #     newuserprofile.last_name = last_name
    #     newuserprofile.username = username
    #     newuserprofile.email = email
    #     newuserprofile.address = request.data["address"]
    #     newuserprofile.picUrl = request.data["picUrl"]
    #     newuserprofile.rollerCoaster_id = request.data["rollercoaster_id"]

    #     newuserprofile.save()
    #     serializer = UserProfileSerializer(newuserprofile, context={'request': request})
    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(
                userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        user = User.objects.get(user=settings.AUTH_USER_MODEL)
        userprofile = UserProfile.objects.get(pk=pk)
        rollercoaster_credits = Credit.objects.get(pk=request.data["credits"])
        first_name = user["first_name"]
        last_name = user["last_name"]
        username = user["username"]
        email = user["email"]

        userprofile.first_name = first_name
        userprofile.last_name = last_name
        userprofile.username = username
        userprofile.email = email
        userprofile.address = request.data["address"]
        userprofile.picUrl = request.data["picUrl"]
        userprofile.rollerCoaster_id = rollercoaster_credits

        # saving userprofile should also save and update the User table.
        # Find on UserProfile models. They are linked together.
        userprofile.save()
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

    def list(self, request):
        userprofiles = UserProfile.objects.all()
        # userprofiles = UserProfile.objects.filter()
        serializer = UserProfileSerializer(
            userprofiles, many=True, context={'request': request})
        return Response(serializer.data)

    # @csrf_exempt
    def login_user(self, request):

        req_body = json.loads(request.body.decode())

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':

            # Use the built-in authenticate method to verify
            username = req_body['username']
            password = req_body['password']
            authenticated_user = authenticate(
                username=username, password=password)

            # If authentication was successful, respond with their token
            if authenticated_user is not None:
                token = Token.objects.get(user=authenticated_user)
                data = json.dumps({"valid": True, "token": token.key})
                return HttpResponse(data, content_type='application/json')

            else:
                # Bad login details were provided. So we can't log the user in.
                data = json.dumps({"valid": False})
                return HttpResponse(data, content_type='application/json')
