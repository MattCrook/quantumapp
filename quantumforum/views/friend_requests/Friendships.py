from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumforum.models import Friendships as FriendshipsModel




class FriendshipsSerializer(serializers.ModelSerializer):
        class Meta:
            model = FriendshipsModel
            fields = ('id', 'requester', 'addressee')
            depth = 1



class Friendships(ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        all_friendships = FriendshipsModel.objects.all()
        requester_id = self.request.query_params.get("sender")
        addressee_id = self.request.query_params.get('addressee')

        if requester_id is not None:
            all_friendships = all_friendships.filter(requester_id=requester_id)

        if addressee_id is not None:
            all_friendships = all_friendships.filter(addressee_id=addressee_id)

        serializer = FriendshipsSerializer(all_friendships, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            friendship = FriendshipsModel.objects.get(pk=pk)
            serializer = FriendshipsSerializer(friendship, context={'request': request})
            return Response(serializer.data)

        except FriendshipsModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            return Response({'message': exc.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None):
        pass
