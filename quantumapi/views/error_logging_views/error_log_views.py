from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ErrorLog as ErrorLogModel
import json
import datetime


class ErrorLogViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLogModel
        fields = ('id', 'user', 'environment', 'error_message', 'stack', 'component', 'calling_function',
                  'key', 'session', 'request_data', 'headers', 'host_ip', 'date')
        depth = 1


class ErrorLogView(ViewSet):

    def list(self, request):
        try:
            data = ErrorLogModel.objects.all()
            user_id = self.request.query_params.get("user_id", None)
            component = self.request.query_params.get("component", None)
            calling_function = self.request.query_params.get("calling_function", None)
            key = self.request.query_params.get("key", None)
            error_message = self.request.query_params.get("error_message", None)

            if user_id is not None:
                data = ErrorLogModel.objects.filter(user_id=user_id)

            if component is not None:
                data = ErrorLogModel.objects.filter(component=component)

            if calling_function is not None:
                data = ErrorLogModel.objects.filter(calling_function=calling_function)

            if key is not None:
                data = ErrorLogModel.objects.filter(key=key)

            if error_message is not None:
                data = ErrorLogModel.objects.filter(error_message=error_message)

            serializer = ErrorLogViewSerializer(
                data, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        try:
            data = ErrorLogModel.objects.get(pk=pk)
            serializer = ErrorLogViewSerializer(
                data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            incoming_req_time = request.data['time']
            date_string = str(incoming_req_time)
            current_hour_and_seconds = date_string.split(" ")[4]

            time = datetime.datetime.utcnow()
            date_strftime = time.strftime("%H:%M:%S")
            date_strftime_string = date_strftime.split(" ")
            print(current_hour_and_seconds)
            print(date_strftime)

            if current_hour_and_seconds != date_strftime:
                user = request.user
                key = request.auth
                authenticators = request.authenticators
                headers = request.stream.headers
                session = request.session

                if session.session_key is None:
                    session = session.cycle_key()
                    print("SESSION", session)

                host_ip = request.META['REMOTE_ADDR']
                environment = request.stream.environ
                resolver_match = request.stream.resolver_match

                new_error_log = ErrorLogModel()
                new_error_log.user = user
                new_error_log.environment = environment
                new_error_log.error_message = request.data['message']
                new_error_log.stack = request.data['stack']
                new_error_log.component = request.data['component']
                new_error_log.calling_function = request.data['callingFunction']
                new_error_log.key = key
                new_error_log.session = session
                new_error_log.request_data = request.data
                new_error_log.headers = headers
                new_error_log.date = datetime.datetime.utcnow()

                new_error_log.save()
                serializer = ErrorLogViewSerializer(new_error_log, context={'request': request})
                return Response(serializer.data)

            else:
                user = request.user
                error_message = request.data['message']
                stack = request.data['stack']
                component = request.data['component']
                calling_function = request.data['callingFunction']
                error_logs = ErrorLogModel.objects.filter(user_id=user.id)

                for entry in error_logs:
                    existing_message = entry.error_message
                    existing_stack = entry.stack
                    existing_component = entry.component
                    existing_calling_function = entry.calling_function

                    if existing_message == error_message and existing_stack == stack and existing_component == component and existing_calling_function == calling_function:
                        return Response({}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None):
        try:
            error_log = ErrorLogModel.objects.get(pk=pk)
            error_log.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ErrorLogModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
