from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.decorators import login_required
from quantumapi.models import BlogContributorApplication as BlogContributorApplicationModel
from quantumapi.models import User as UserModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
import datetime



class BlogApplicationSerializer(serializers.ModelSerializer):
        class Meta:
            model = BlogContributorApplicationModel
            url = serializers.HyperlinkedIdentityField(
                view_name='blogcontributorapplication',
                lookup_field='id'
            )
            fields = ('id', 'user', 'first_name', 'last_name', 'email', 'social_media', 'short_description', 'date_submitted')
            depth = 1




class BlogContributorApplications(ViewSet):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def list(self, request):
        all_submissions= BlogContributorApplicationModel.objects.all()
        serializer = BlogApplicationSerializer(all_submissions, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            submission = BlogContributorApplicationModel.objects.get(pk=pk)
            serializer = BlogApplicationSerializer(submission, context={'request': request})
            return Response(serializer.data)

        except BlogContributorApplicationModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response({'message': exc.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            new_submission = BlogContributorApplicationModel()
            user = UserModel.objects.get(pk=request.data['user_id'])
            date = datetime.datetime.now()

            new_submission.user = user
            new_submission.first_name = request.data["firstName"]
            new_submission.last_name = request.data["lastName"]
            new_submission.email = request.data["email"]
            new_submission.social_media = request.data["socialMedia"]
            new_submission.short_description = request.data["shortDescription"]
            new_submission.date_submitted = date

            new_submission.save()
            serializer = BlogApplicationSerializer(new_submission, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            submission = BlogContributorApplicationModel.objects.get(pk=pk)
            submission.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except BlogContributorApplicationModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
