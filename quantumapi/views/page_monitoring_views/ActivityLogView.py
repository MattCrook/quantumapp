from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ActivityLog as ActivityLogModel
import json
import datetime



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
            user = UserModel.objects.get(pk=request.data['event']['user_id'])
            req_date = request.data['event']['date']

            is_activity_log = ActivityLogModel.objects.filter(user_id=user.id).exists()


            # Filter activity log list by user_id, if returns true, then grab that list.
            # Else, no actions yet for user (probably new user), or no actions yet for that date, so create new instance.
            if is_activity_log:
                all_user_activity = ActivityLogModel.objects.filter(user_id=user.id)
                user_activity_for_incoming_date = []
                new_date = []

                # Loop over the object and look at date attribute and look for match
                # Matching to determine if same day/ session, if date matches then we will add to array of
                # actions user takes during that day/ session.

                for action in all_user_activity:
                    date_time = action.date
                    date_strftime = date_time.strftime("%d %m %Y  (%H:%M:%S.%f)")
                    date_strftime_string = date_strftime.split(" ")
                    day = date_strftime_string[0]
                    month = date_strftime_string[1]
                    year = date_strftime_string[2]
                    date = f"{year}-{month}-{day}"

                    if req_date == date:
                        user_activity_for_incoming_date.append(action)
                    else:
                        new_date.append(request.data)

                # Matching object will be in an array so take first index.
                # Get the ID of object and extract the resource from DB.
                # Grab reference to existing object, push into array,
                # Then take incoming action object and append to the array as well. Creating
                # and array of objects of actions for the user.
                if len(user_activity_for_incoming_date) > 0:
                    activity_log_object = user_activity_for_incoming_date[0]
                    activity_log = add_action_to_existing_actions(request, activity_log_object)

                elif len(new_date) > 0:
                    activity_log_object = new_date[0]
                    activity_log = create_new_action(request, user, activity_log_object)

                return Response(activity_log.data)

            else:
                new_activity_log = ActivityLogModel()
                new_activity_log.user = user
                req_data_actions = request.data['event']['action']
                serialized_actions = json.dumps({'event': req_data_actions})
                new_activity_log.action = serialized_actions

                new_activity_log.save()
                serializer = ActivityLogSerializer(new_activity_log, context={'request': request})
                return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            activity_log = ActivityLogModel.objects.get(pk=pk)
            activity_log.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ActivityLogModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def add_action_to_existing_actions(request, activity_log_action):
    try:
        activity_log_id = activity_log_action.id
        activity_log = ActivityLogModel.objects.get(pk=activity_log_id)

        actions = json.loads(activity_log.action)
        events = actions['event']
        new_action = request.data['event']['action']
        events_list = []

        if isinstance(events, list) and len(events) > 1:
            events_list = events
            print("Events 2", events_list)
            events_list.append(new_action)
        else:
            events_list.append(events)
            events_list.append(new_action)

        actions['event'] = events_list
        activity_log.action = json.dumps(actions)
        activity_log.save()
        serializer = ActivityLogSerializer(activity_log, context={'request': request})
        return serializer

    except Exception as ex:
        return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_new_action(request, user, activity_log_action):
    try:
        new_activity_log = ActivityLogModel()
        new_activity_log.user = user
        req_data_actions = request.data['event']['action']
        serialized_actions = json.dumps({'event': req_data_actions})
        new_activity_log.action = serialized_actions

        new_activity_log.save()
        serializer = ActivityLogSerializer(new_activity_log, context={'request': request})
        return serializer

    except Exception as ex:
        return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
