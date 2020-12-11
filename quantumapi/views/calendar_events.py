from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.decorators import login_required
from quantumapi.models import CalendarEvent as CalendarEventModel
from quantumapi.models import User as UserModel
import datetime



class CalendarEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = CalendarEventModel
            url = serializers.HyperlinkedIdentityField(
                view_name='calendarevent',
                lookup_field='id'
            )
            fields = ('id', 'user', 'title', 'location', 'description', 'time', 'date', 'is_reminder_set', 'reminder_value')
            depth = 1

class CalendarEvents(ViewSet):
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
            user = UserModel.objects.get(pk=request.data['user_id'])

            new_calendar_event.user = user
            new_calendar_event.title = request.data["title"]
            new_calendar_event.location = request.data["location"]
            new_calendar_event.description = request.data["description"]
            new_calendar_event.time = request.data["time"]
            new_calendar_event.date = request.data["date"]
            new_calendar_event.is_reminder_set = request.data["is_reminder_set"]
            new_calendar_event.reminder_value = request.data["reminder_value"]

            new_calendar_event.save()

            serializer = CalendarEventSerializer(new_calendar_event, context={'request': request})
            return Response(serializer.data)

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
