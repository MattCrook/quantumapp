from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import Credit, RollerCoaster, UserProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from .rollerCoaster import RollerCoasterSerializer




class CreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['id', 'userProfile', 'rollerCoaster']
        depth = 1


class Credits(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def retrieve(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk)
            serializer = CreditsSerializer(credit, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    # Handle GET request to Credits resource.
    def list(self, request):
        try:
            all_credits = Credit.objects.all()
            # If credits is provided as a query parameter, then filter list of credits by userprofile id
            # credit = self.request.query_params.get('profile', None)
            # Get the extended table of user with the user profile table

            serializer = CreditsSerializer(all_credits, many=True, context={'request': request})
            return Response(serializer.data)

        except Credit.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        new_credit = Credit()
        rollercoaster = RollerCoaster.objects.get(pk=request.data["rollerCoaster_id"])
        userprofile = UserProfile.objects.get(pk=request.data["userProfile_id"])

        new_credit.userProfile = userprofile
        new_credit.rollerCoaster = rollercoaster

        new_credit.save()
        serializer = CreditsSerializer(new_credit, context={'request': request})

        return Response(serializer.data)


    def destroy(self, request, pk=None):
        try:
            credit = Credit.objects.get(pk=pk)
            credit.delete()
            return Response({'Deleted': credit.id}, status=status.HTTP_204_NO_CONTENT)

        except Credit.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
