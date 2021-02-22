from rest_framework.authentication import authenticate, SessionAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumforum.models import FriendRequest as FriendRequestModel
from quantumforum.models import Friendships as FriendshipsJoin
from quantumforum.models import StatusCode as StatusCodeModel
from quantumapi.models import UserProfile as UserProfileModel
from django.contrib.auth import get_user_model
import datetime





class FriendRequestSerializer(serializers.ModelSerializer):
        class Meta:
            model = FriendRequestModel
            fields = ('id', 'sender_and_receiver', 'status_code', 'last_updated_by', 'sent_date', 'last_updated')
            depth = 2



class FriendRequests(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        all_friend_requests = FriendRequestModel.objects.all()
        serializer = FriendRequestSerializer(all_friend_requests, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            submission = FriendRequestModel.objects.get(pk=pk)
            serializer = FriendRequestSerializer(submission, context={'request': request})
            return Response(serializer.data)

        except FriendRequestModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response({'message': exc.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            UserModel = get_user_model()
            sender_user = request.user
            receiver_id = request.data['receiver']
            receiver_user_profile = UserProfileModel.objects.get(pk=receiver_id)
            receiver = UserModel.objects.get(pk=receiver_user_profile.user_id)

            friendship = FriendshipsJoin()
            friendship.requester = sender_user
            friendship.addressee = receiver
            friendship.save()

            new_friend_request = FriendRequestModel()
            new_friend_request.sender_and_receiver = friendship
            new_friend_request.status_code = StatusCodeModel.objects.get(code=request.data['statusCode'])
            new_friend_request.last_updated_by = UserModel.objects.get(pk=request.data['lastUpdatedBy'])
            new_friend_request.date = datetime.datetime.now()
            new_friend_request.save()

            serializer = FriendRequestSerializer(new_friend_request, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request):
        try:
            UserModel = get_user_model()
            friend_request = FriendRequestModel.objects.get(pk=request.data['id'])

            if 'statusCode' in request.data and request.data['statusCode']:
                status_code = StatusCodeModel.objects.get(pk=request.data['statusCode'])
                friend_request.status_code = status_code

            if 'lastUpdatedBy' in request.data and request.data['lastUpdatedBy']:
                last_updated_by = UserModel.objects.get(pk=request.data['lastUpdatedBy'])
                friend_request.last_updated_by = last_updated_by

            friend_request.last_updated = datetime.datetime.now()
            friend_request.save()
            return Response({"Success": True}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            submission = FriendRequestModel.objects.get(pk=pk)
            submission.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except FriendRequestModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
