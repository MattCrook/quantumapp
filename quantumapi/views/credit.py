from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Credit, RollerCoaster, UserProfile
from django.contrib.auth.models import User


class CreditsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Credit
        url = serializers.HyperlinkedIdentityField(
            view_name='credit',
            lookup_field='id'
        )
        fields = ('id', 'url', 'userProfile', 'rollerCoaster', )
        depth = 0


class Credits(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk)
            serializer = CreditsSerializer(credit, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handle GET request to Credits resource.
    # Would be a GET request to UserProfile resource and need to GET all credits the user has."""
    def list(self, request):

        # all_credits = list(Credit.objects.all())
        # print("ALLCREDITS", all_credits)
        # all_userprofiles = UserProfile.objects.all()

        # If credits is provided as a query parameter, then filter list of credits by userprofile id
        # credit = self.request.query_params.get('profile', None)
        # Get the extended table of user with the user profile table
        # user_profile = request.user.profile

        userprofile = UserProfile.objects.get(pk=request.user.profile.id)
        user_credits = Credit.objects.filter(userProfile=userprofile)

        serializer = CreditsSerializer(user_credits, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        rollercoaster = RollerCoaster.objects.get(pk=request.data["rollercoaster_id"])
        userprofile = UserProfile.objects.get(pk=request.data["userprofile_id"])

        new_credit = Credit()
        new_credit.userprofile = userprofile
        new_credit.rollercoaster = rollercoaster

        new_credit.save()
        serializer = CreditsSerializer(new_credit, context={'request': request})

        return Response(serializer.data)


    def update(self, request):
        credit = Credit.objects.get(pk=pk)
        rollercoaster = RollerCoaster.objects.get(pk=request.data["rollercoaster_id"])
        userprofile = UserProfile.objects.get(pk=request.data["userprofile_id"])

        credit.userprofile = userprofile
        credit.rollercoaster = rollercoaster

        credit.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk)
            credit.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Credit.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
