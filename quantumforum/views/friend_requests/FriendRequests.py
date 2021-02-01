from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumforum.models import FriendRequest as FriendRequestModel
from quantumforum.models import Friendships as FriendshipsJoin
from quantumforum.models import StatusCode as StatusCodeModel
from django.contrib.auth import get_user_model
import datetime





class FriendRequestSerializer(serializers.ModelSerializer):
        class Meta:
            model = FriendRequestModel
            fields = ('id', 'sender_and_receiver', 'status_code', 'last_updated_by')
            depth = 2



class FriendRequests(ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

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
            new_friend_request = FriendRequestModel()
            sender_user = request.user
            receiver_user_id = request.data['receiver']
            receiver_user = UserModel.objects.get(pk=receiver_user_id)

            friendship = FriendshipsJoin()
            friendship.requester = sender_user
            friendship.addressee = receiver_user
            friendship.save()

            status_code = StatusCodeModel.objects.get_or_create(code=0)
            status_code.save()


            new_friend_request.sender_and_receiver = friendship.id
            new_friend_request.status_code = status_code
            new_friend_request.last_updated_by = request.data['actionTakenBy']
            new_friend_request.date = datetime.datetie.now()
            new_friend_request.save()

            serializer = FriendRequestSerializer(new_friend_request, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request):
        pass


    def destroy(self, request, pk=None):
        try:
            submission = FriendRequestModel.objects.get(pk=pk)
            submission.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except FriendRequestModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(('GET', 'POST'))
# @authentication_classes([SessionAuthentication, JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def friend_request_view(request):
#     pass
