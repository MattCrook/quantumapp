from rest_framework.authentication import authenticate, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from quantumforum.models import FriendsJoin as FriendsJoinModel
from django_filters.rest_framework import DjangoFilterBackend
import datetime


class FriendsJoinSerializer(serializers.ModelSerializer):
        class Meta:
            model = FriendsJoinModel
            fields = ('id', 'users_friends', 'friend_request')
            depth = 2



class FriendsJoinApiView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = FriendsJoinModel.objects.all()
    serializer_class = FriendsJoinSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['friend_request']
