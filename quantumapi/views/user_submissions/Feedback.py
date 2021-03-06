from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from quantumapi.models import Feedback as FeedbackModel
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackModel
        fields = ('id', 'subject', 'feedback', 'date', 'user')
        depth = 1


class Feedback(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        all_feedback_submissions = FeedbackModel.objects.all()
        serializer = FeedbackSerializer(all_feedback_submissions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        try:
            user = request.user
            new_feedback_submission = FeedbackModel()
            new_feedback_submission.subject = request.data['subject']
            new_feedback_submission.feedback = request.data['comment']
            new_feedback_submission.date = datetime.datetime.now()
            new_feedback_submission.user = user
            new_feedback_submission.save()

            serializer = FeedbackSerializer(new_feedback_submission, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'Error:': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            feedback_submission = FeedbackModel.objects.get(pk=pk)
            serializer = FeedbackSerializer(feedback_submission, context={'request': request})
            return Response(serializer.data)
        except FeedbackModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
