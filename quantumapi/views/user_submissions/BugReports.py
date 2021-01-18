from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from quantumapi.models import BugReport as BugReportModel
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime



class BugReportsSerializer(serializers.ModelSerializer):
        class Meta:
            model = BugReportModel
            fields = ('id', 'title', 'description', 'date', 'user')
            depth = 1


class BugReports(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        try:
            all_bug_reports = BugReportModel.objects.all()
            serializer = BugReportsSerializer(all_bug_reports, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"Error: ": ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            user = request.user
            new_bug_report = BugReportModel()
            new_bug_report.title = request.data['title']
            new_bug_report.description = request.data['description']
            new_bug_report.date = datetime.datetime.now()
            new_bug_report.user = user
            new_bug_report.save()

            serializer = BugReportsSerializer(new_bug_report, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'Error:': ex.args}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            bug_report = BugReportModel.objects.get(pk=pk)
            serializer = BugReportsSerializer(bug_report, context={'request': request})
            return Response(serializer.data)
        except BugReportModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
