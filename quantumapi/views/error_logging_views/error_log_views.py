from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ErrorLog as ErrorLogModel
from django.contrib.sessions.models import Session
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
                data = ErrorLogModel.objects.filter(
                    calling_function=calling_function)

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
            serializer = ErrorLogViewSerializer(data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            incoming_req_time = request.data['time']
            date_string = str(incoming_req_time)
            current_hour_and_seconds_from_request = date_string.split(" ")[4]
            time = datetime.datetime.utcnow()
            date_strftime = time.strftime("%H:%M:%S")
            date_strftime_string = date_strftime.split(" ")

            if request.session.session_key is None:
                session = Session.objects.get(session_key=request.data['sessionId'])
            else:
                session = request.session.session_key

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
                            resolver_match = request.stream.resolver_match
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
            error_log = ErrorLogModel.objects.get(pk=log.id)
            error_log.user = request.user
            error_log.environment = request.stream.environ
            error_log.error_message = request.data['message']
            error_log.stack = request.data['stack']
            error_log.component = request.data['component']
            error_log.calling_function = request.data['callingFunction']
            error_log.key = request.auth
            error_log.session = session.session_key
            error_log.request_data = request.data
            error_log.headers = request.stream.headers
            error_log.host_ip = request.META['REMOTE_ADDR']
            error_log.date = time

            error_log.save()
            serialized_updated_log = ErrorLogViewSerializer(error_log, context={'request': request})
            schemas.add(serialized_updated_log)

        serializer = list(schemas)
        return serializer[0]

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def create_new_error_log_entry(request, session, time):
    try:
        new_error_log = ErrorLogModel()
        new_error_log.user = request.user
        new_error_log.environment = request.stream.environ
        new_error_log.error_message = request.data['message']
        new_error_log.stack = request.data['stack']
        new_error_log.component = request.data['component']
        new_error_log.calling_function = request.data['callingFunction']
        new_error_log.key = request.auth
        new_error_log.session = session.session_key
        new_error_log.request_data = request.data
        new_error_log.headers = request.stream.headers
        new_error_log.host_ip = request.META['REMOTE_ADDR']
        new_error_log.date = time

        new_error_log.save()
        serializer = ErrorLogViewSerializer(new_error_log, context={'request': request})
        return serializer
    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def update_or_create(request, data, session, time):
    try:
        if 'existing_logs_matched' in data and len(data['existing_logs_matched']) > 0:
            existing_logs_matched = data['existing_logs_matched']
            serializer = update_existing_entry_with_latest_data(request, existing_logs_matched, session, time)

        elif 'unique_times' in data and len(data['unique_times']) > 0:
            serializer = create_new_error_log_entry(request, session, time)

        return serializer

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
