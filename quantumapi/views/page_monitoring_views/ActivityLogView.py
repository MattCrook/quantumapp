from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ActivityLog as ActivityLogModel



class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogModel
        url = serializers.HyperlinkedIdentityField(view_name='activitylog', lookup_field='id')
        fields = ('id', 'user', 'action', 'date')
        depth = 1

class ActivityLogView(ViewSet):

    def list(self, request):
        data = ActivityLogModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = ActivityLogModel.objects.filter(user_id=user_id)

        serializer = ActivityLogSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            data = ActivityLogModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);
            if user_id is not None:
                data = ActivityLogModel.objects.filter(user_id=user_id)

            serializer = ActivityLogSerializer(data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            activity_log = ActivityLogModel()
            user = UserModel.objects.get(pk=request.data['user_id'])

            activity_log.user = user
            activity_log.action = request.data["email"]

            activity_log.save()
            serializer = ActivityLogSerializer(activity_log, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            activity_log = ActivityLogModel.objects.get(pk=pk)
            activity_log.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ActivityLogModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
