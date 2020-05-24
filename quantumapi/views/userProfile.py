from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import UserProfile, Credit
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import authentication, permissions



class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserProfile
        url = serializers.HyperlinkedIdentityField(
            view_name='userprofile',
            lookup_field='id'
        )
        fields = ('id', 'url', 'address', 'picUrl', )
        depth = 1


class UserProfiles(ViewSet):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [authentication.TokenAuthentication]


    # def get(self, request, format=None):
    #     """
    #     Return a list of all users.
    #     """
    #     emails = [user.email for user in User.objects.all()]
    #     return Response(emails)
    # serializer_class = UserProfileSerializer
    # permission_classes = (IsAuthenticated,)

    def create(self, request):
        user = User.objects.get(user=request.auth.user)
        first_name = user["first_name"]
        last_name = user["last_name"]
        username = user["username"]
        email = user["email"]
        rollerCoaster_id = Credit.objects.get(pk="credits")

        newuserprofile = UserProfile()
        newuserprofile.first_name = first_name
        newuserprofile.last_name = last_name
        newuserprofile.username = username
        newuserprofile.email = email
        newuserprofile.address = request.data["address"]
        newuserprofile.picUrl = request.data["picUrl"]
        newuserprofile.rollerCoaster_id = request.data["rollercoaster_id"]

        newuserprofile.save()
        serializer = UserProfileSerializer(newuserprofile, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            userprofile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(userprofile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        user = User.objects.get(user=request.auth.user)
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
        serializer = UserProfileSerializer(userprofiles, many=True, context={'request': request})
        return Response(serializer.data)
