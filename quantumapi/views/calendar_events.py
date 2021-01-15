from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.decorators import login_required
from quantumapi.models import CalendarEvent as CalendarEventModel
from quantumapi.models import User as UserModel
from django.contrib.sessions.models import Session
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime




class CalendarEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = CalendarEventModel
            url = serializers.HyperlinkedIdentityField(
                view_name='calendarevent',
                lookup_field='id'
            )
            fields = ('id', 'user', 'title', 'location', 'description', 'start_time', 'end_time', 'date', 'is_reminder_set', 'reminder_value')
            depth = 1

class CalendarEvents(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        all_calendar_events = CalendarEventModel.objects.all()
        serializer = CalendarEventSerializer(all_calendar_events, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            calendar_event = CalendarEventModel.objects.get(pk=pk)
            serializer = CalendarEventSerializer(calendar_event, context={'request': request})
            return Response(serializer.data)

        except CalendarEventModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response({'message': exc.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            new_calendar_event = CalendarEventModel()
            user = request.user
            # session = request.stream.session
            # auth = request.auth

            new_calendar_event.user = user
            new_calendar_event.title = request.data["title"]
            new_calendar_event.location = request.data["location"]
            new_calendar_event.description = request.data["description"]
            new_calendar_event.start_time = request.data["startTime"]
            new_calendar_event.end_time = request.data["endTime"]
            new_calendar_event.date = datetime.date.today()
            new_calendar_event.is_reminder_set = request.data["isReminderSet"]

            if "reminderValue" in request.data and request.data["reminderValue"]:
                new_calendar_event.reminder_value = request.data["reminderValue"]
            else:
                new_calendar_event.reminder_value = "No Reminders"

            new_calendar_event.save()

            serializer = CalendarEventSerializer(new_calendar_event, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            calendar_event = CalendarEventModel.objects.get(pk=pk)
            user = request.user

            calendar_event.user = user
            calendar_event.title = request.data["title"]
            calendar_event.location = request.data["location"]
            calendar_event.description = request.data["description"]
            calendar_event.start_time = request.data["startTime"]
            calendar_event.end_time = request.data["endTime"]
            calendar_event.date = datetime.date.today()
            calendar_event.is_reminder_set = request.data["isReminderSet"]

            if "reminderValue" in request.data and request.data["reminderValue"]:
                calendar_event.reminder_value = request.data["reminderValue"]
            else:
                calendar_event.reminder_value = "No Reminders"

            calendar_event.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def destroy(self, request, pk=None):
        try:
            calendar_event = CalendarEventModel.objects.get(pk=pk)
            calendar_event.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CalendarEventModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
