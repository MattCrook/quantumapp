from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import ActivityLog as ActivityLogModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import json
import datetime



class ActivityLogSerializer(serializers.ModelSerializer):

    user = serializers.DictField()
    action = serializers.DictField()
    date = serializers.DateTimeField()

    class Meta:
        model = ActivityLogModel
        fields = ('id', 'user', 'action', 'date')
        depth = 1

class ActivityLogView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        data = ActivityLogModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = ActivityLogModel.objects.filter(user_id=user_id)

        activity_log_queryset = []

        for instance in data:
            activity_log_instance = {
                "id": instance.id,
                "user": instance.user.to_dict(),
                "action": json.loads(instance.action),
                "date": instance.date,
            }
            serializer = ActivityLogSerializer(data=activity_log_instance, context={'request': request})
            valid = serializer.is_valid()
            if valid:
                activity_log_queryset.append(serializer.data)
            else:
                return Response(serializer.errors)

        serializer = ActivityLogSerializer(activity_log_queryset, many=True, context={'request': request})
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
            user = UserModel.objects.get(pk=request.data["event"]["user_id"])
            req_date = request.data["event"]["date"]

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
                    activity_log_serializer = add_action_to_existing_actions(request, activity_log_object)

                elif len(new_date) > 0:
                    activity_log_object = new_date[0]
                    activity_log_serializer = create_new_action(request, user, activity_log_object)

                return Response(activity_log_serializer.data)

            else:
                new_activity_log = ActivityLogModel()
                new_activity_log.user = user
                req_data_actions = request.data["event"]["action"]
                actions = json.dumps({"event": req_data_actions})
                new_activity_log.action = actions
                new_activity_log.date = datetime.datetime.now()
                new_activity_log.save()

                data = {
                    "user": user.to_dict(),
                    "action": json.loads(actions),
                    "date": datetime.datetime.now()
                }

                serializer = ActivityLogSerializer(data=data, context={'request': request})
                valid = serializer.is_valid()

                if valid:
                    return Response(serializer.data)
                else:
                    return Response({'Serializer Errors': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        events = actions["event"]
        new_action = request.data["event"]["action"]
        events_list = []

        if isinstance(events, list) and len(events) > 1:
            events_list = events
            events_list.append(new_action)
        else:
            events_list.append(events)
            events_list.append(new_action)

        actions["event"] = events_list
        activity_log.action = json.dumps(actions)
        activity_log.save()

        data = {
            "user": request.user.to_dict(),
            "action": json.loads(actions),
            "date": datetime.datetime.now()
        }
        serializer = ActivityLogSerializer(data=data, context={'request': request})
        valid = serializer.is_valid()
        if valid:
            return serializer
        else:
            return serializer.errors

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_new_action(request, user, activity_log_action):
    try:
        new_activity_log = ActivityLogModel()
        new_activity_log.user = user
        req_data_actions = request.data["event"]["action"]
        actions = json.dumps({"event": req_data_actions})
        new_activity_log.action = actions
        new_activity_log.save()

        data = {
            "user": user.to_dict(),
            "action": json.loads(actions),
            "date": datetime.datetime.now()
        }
        serializer = ActivityLogSerializer(data=data, context={'request': request})
        valid = serializer.is_valid()
        if valid:
            return serializer
        else:
            return serializer.errors

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
