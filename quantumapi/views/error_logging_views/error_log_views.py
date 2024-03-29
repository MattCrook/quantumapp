from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
# from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ErrorLog as ErrorLogModel
from quantumapi.models import Credential as CredentialModel
from django.contrib.sessions.models import Session
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json
import datetime
import socket
# from collections import OrderedDict


class ErrorLogViewSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(label='ID')
    user = serializers.DictField()
    environment = serializers.DictField()
    error_message = serializers.CharField()
    stack = serializers.CharField()
    environment = serializers.DictField()
    component = serializers.CharField()
    calling_function = serializers.CharField()
    key = serializers.CharField()
    session = serializers.CharField()
    request_data = serializers.DictField()
    headers = serializers.DictField()
    host_ip = serializers.CharField()
    date = serializers.DateTimeField()


    class Meta:
        model = ErrorLogModel
        fields = ('id', 'user', 'environment', 'error_message', 'stack', 'component', 'calling_function', 'key', 'session', 'request_data', 'headers', 'host_ip', 'date')
        depth = 1


class ErrorLogView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        try:
            error_log_queryset = ErrorLogModel.objects.all()
            user_id = self.request.query_params.get("user_id", None)
            component = self.request.query_params.get("component", None)
            calling_function = self.request.query_params.get("calling_function", None)
            key = self.request.query_params.get("key", None)
            error_message = self.request.query_params.get("error_message", None)

            if user_id is not None:
                error_log_queryset = ErrorLogModel.objects.filter(user_id=user_id)

            if component is not None:
                error_log_queryset = ErrorLogModel.objects.filter(component=component)

            if calling_function is not None:
                error_log_queryset = ErrorLogModel.objects.filter(calling_function=calling_function)

            if key is not None:
                error_log_queryset = ErrorLogModel.objects.filter(key=key)

            if error_message is not None:
                error_log_queryset = ErrorLogModel.objects.filter(error_message=error_message)

            serialized_data = []
            for instance in error_log_queryset:

                error_log = {
                    "id": instance.id,
                    "user": instance.user.to_dict(),
                    "environment": json.loads(instance.environment),
                    "error_message": instance.error_message,
                    "stack": instance.stack,
                    "component": instance.component,
                    "calling_function": instance.calling_function,
                    "key": instance.key,
                    "session": instance.session,
                    "request_data": json.loads(instance.request_data),
                    "headers": json.loads(instance.headers),
                    "host_ip": instance.host_ip,
                    "date": instance.date
                }

                serializer = ErrorLogViewSerializer(data=error_log, context={'request': request})
                if serializer.is_valid() is True:
                    serialized_data.append(serializer.data)
                else:
                    return Response({'Serializer Error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = ErrorLogViewSerializer(serialized_data, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        try:
            data = ErrorLogModel.objects.get(pk=pk)

            instance = {
                "id": data.id,
                "user": data.user.to_dict(),
                "environment": json.loads(data.environment),
                "error_message": data.error_message,
                "stack": data.stack,
                "component": data.component,
                "calling_function": data.calling_function,
                "key": data.key,
                "session": data.session,
                "request_data": json.loads(data.request_data),
                "headers": json.loads(data.headers),
                "host_ip": data.host_ip,
                "date": data.date
            }

            serializer = ErrorLogViewSerializer(data=instance, context={'request': request})
            if serializer.is_valid() is True:
                return Response(serializer.data)
            else:
                return serializer.errors
        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            incoming_req_time = request.data['time']
            date_string = str(incoming_req_time)
            current_hour_and_seconds_from_request = date_string.split(" ")[4]
            time = datetime.datetime.utcnow()
            date_strftime = time.strftime("%H:%M:%S")
            date_strftime_string = date_strftime.split(" ")

            if request.session is not None:
                if request.session.session_key is not None:
                    session = request.session.session_key
                else:
                    session = CredentialModel.objects.filter(user_id=request.user.id).latest().session_id if CredentialModel.objects.filter(user_id=request.user.id).exists() else 'no session data'
                    # session = credential.session_id
            elif Session.objects.filter(session_key=request.data['sessionId']).exists():
                session = Session.objects.get(session_key=request.data['sessionId'])
            else:
                session = 'no session data'

            try:
                # if incoming date (from client) does not match current date (set on backend) then skip.
                # Checking for duplicates here, as frontend is going to re render multiple times to hydrate the page.
                # As a result, the same error request is sent multiple times as the client re renders before having the data it needs.
                # This serves as initial check, guard to check if it is a new request, or duplicate request.
                # Needs to be == , because first request will be the equal time, and each subsequent request will take longer,
                # Thus the times will be off and sending it to the else: block.
                if current_hour_and_seconds_from_request != date_strftime:
                    try:
                        user = request.user

                        # Check to see if user has existing logs in DB.
                        # Doing this fo later to check for duplicates.
                        user_has_logs = ErrorLogModel.objects.filter(user_id=user.id).exists()

                        if user_has_logs:
                            user_logs = ErrorLogModel.objects.filter(user_id=user.id)
                            data = is_existing_log_entry(request, user, date_strftime)
                            serializer = update_or_create(request, data, session, time)

                        else:
                            # ToDo: add resolver match to field in Model.
                            # resolver_match = request.stream.resolver_match
                            serializer = create_new_error_log_entry(request, session, time)

                        return Response(serializer.data)

                    except Exception as ex:
                        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    user = request.user
                    user_has_logs = ErrorLogModel.objects.filter(user_id=user.id).exists()

                    if user_has_logs:
                        user_logs = ErrorLogModel.objects.filter(user_id=user.id)
                        data = is_existing_log_entry(request, user, date_strftime)
                        serializer = update_or_create(request, data, session, time)

                    else:
                        serializer = create_new_error_log_entry(request, session, time)

                    return Response(serializer.data)

            except Exception as ex:
                return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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




def is_existing_log_entry(request, user, date_strftime):
    """
    If check to see if user has entries already in the database, then this
    function can be called to filter all the users entries,
    then by calling 'filtered_matching_user_logs' returns a dict 
    containing two arrays, one for matching queries with non-matching timestamps,
    and one for matching timestamps.
    """
    key = request.auth
    authenticators = request.authenticators
    headers = request.stream.headers
    user_logs = ErrorLogModel.objects.filter(user_id=user.id)
    data = filtered_matching_user_logs(request, user_logs, date_strftime)
    return data




def filtered_matching_user_logs(request, user_logs, date_strftime):
    '''
    Filtering on all the logs user has posted, and looping through them
    to compare incoming request to each item in the loop. The, compares time stamps
    to then build a dict to return of matching items with matching time stamps, and
    matching items without matching timestamps. The former will be an update, the latter
    will be a new entry.
     '''

    req_data_message = request.data['message']
    req_data_stack = request.data['stack']
    req_data_component = request.data['component']
    req_data_calling_function = request.data['callingFunction']
    existing_logs_matched_to_req_data = []
    duplicate_requests_unique_times = []
    data = dict()

    for log_entry in user_logs:
        existing_message = log_entry.error_message
        existing_stack = log_entry.stack
        existing_component = log_entry.component
        existing_calling_function = log_entry.calling_function
        existing_date = log_entry.date

        # Comparing the current item against the incoming request data.
        # If all these fields match, then if the time matches, it is indeed a real duplicate.
        # If all these items match, and time does not,
        # it is perhaps a subsequent request, but one that should be logged.
        if existing_message == req_data_message and existing_stack == req_data_stack and existing_component == req_data_component and existing_calling_function == req_data_calling_function:
            log_entry_date = log_entry.date.strftime("%H:%M:%S")

            # Grabbing none-time matches because if times match then it is 100% match meaning within same request.
            # If time matches, then don't need to post, bc entry already exists.
            if date_strftime == log_entry_date:
                existing_logs_matched_to_req_data.append(log_entry)

            elif date_strftime != log_entry_date:
                duplicate_requests_unique_times.append(log_entry)

    data['existing_logs_matched'] = existing_logs_matched_to_req_data
    data['unique_times'] = duplicate_requests_unique_times
    return data



def update_existing_entry_with_latest_data(request, user_error_logs, session, time):
    """
    Loops through the list of logs specific to the user passed in,
    wil be possibly getting duplicate entries because of front end re-rendering,
    so the items are put into a Set, then turned into a list to only grab unique entries.
    """
    try:
        schemas = set()

        for log in user_error_logs:
            ipv4s = socket.gethostbyname_ex(socket.gethostname())[-1]
            headers = {key: value for (key, value) in request.stream.headers.items()}
            headers_to_dict = dict(headers)
            headers_to_str = json.dumps(headers_to_dict)

            error_log = ErrorLogModel.objects.get(pk=log.id)
            error_log.user = request.user
            error_log.environment = json.dumps({"stream": request.stream.META})
            error_log.error_message = request.data['message']
            error_log.stack = request.data['stack']
            error_log.component = request.data['component']
            error_log.calling_function = request.data['callingFunction']
            error_log.key = request.auth
            error_log.session = session
            error_log.request_data = json.dumps(request.data)
            error_log.headers = headers_to_str
            error_log.host_ip = ipv4s[-1]
            error_log.date = time

            data = {
                "id": error_log.id,
                "user": request.user.to_dict(),
                "environment": {"stream": request.stream.META},
                "error_message": request.data['message'],
                "stack": request.data['stack'],
                "component": request.data['component'],
                "calling_function": request.data['callingFunction'],
                "key": request.auth,
                "session": session,
                "request_data": request.data,
                "headers": headers,
                "host_ip": ipv4s[-1],
                "date": time,
            }

        serializer = ErrorLogViewSerializer(data=data, context={'request': request})
        if serializer.is_valid() is True:
            error_log.save()
            schemas.add(serializer)

        serializer = list(schemas)
        return serializer[0]

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def create_new_error_log_entry(request, session, time):
    try:
        ipv4s = socket.gethostbyname_ex(socket.gethostname())[-1]

        headers = {key: value for (key, value) in request.stream.headers.items()}
        headers_to_dict = dict(headers)
        headers_to_str = json.dumps(headers_to_dict)

        new_error_log = ErrorLogModel()
        new_error_log.user = request.user
        new_error_log.environment = json.dumps({"stream": request.stream.META})
        new_error_log.error_message = request.data['message']
        new_error_log.stack = request.data['stack']
        new_error_log.component = request.data['component']
        new_error_log.calling_function = request.data['callingFunction']
        new_error_log.key = request.auth
        new_error_log.session = session
        new_error_log.request_data = json.dumps(request.data)
        new_error_log.headers = headers_to_str
        new_error_log.host_ip = ipv4s[-1]
        new_error_log.date = time
        new_error_log.save()

        data = {
            "id": new_error_log.id,
            "user": request.user.to_dict(),
            "environment": {"stream": request.stream.META},
            "error_message": request.data['message'],
            "stack": request.data['stack'],
            "component": request.data['component'],
            "calling_function": request.data['callingFunction'],
            "key": request.auth,
            "session": session,
            "request_data": request.data,
            "headers": headers,
            "host_ip": ipv4s[-1],
            "date": time,
        }


        serializer = ErrorLogViewSerializer(data=data, context={'request': request})
        if serializer.is_valid() is True:
            return serializer
        else:
            return serializer.errors
    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def update_or_create(request, data, session, time):
    try:
        if 'existing_logs_matched' in data and data['existing_logs_matched'] and len(data['existing_logs_matched']) > 0:
            existing_logs_matched = data['existing_logs_matched']
            serialized_data = update_existing_entry_with_latest_data(request, existing_logs_matched, session, time)

        elif 'unique_times' in data and data['unique_times'] and len(data['unique_times']) > 0:
            serialized_data = create_new_error_log_entry(request, session, time)

        else:
            empty_response = return_empty_response(data)
            serialized_data = empty_response

        return serialized_data
    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def return_empty_response(data):
    return Response(data, status=status.HTTP_200_OK)
