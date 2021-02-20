from rest_framework.authentication import authenticate, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from quantumforum.models import UsersFriends as UsersFriendsModel
from django_filters.rest_framework import DjangoFilterBackend
import datetime


class UsersFriendsSerializer(serializers.ModelSerializer):
        class Meta:
            model = UsersFriendsModel
            fields = ('id', 'user_profile', 'friends')
            depth = 2



class UsersFriendsApiView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = UsersFriendsModel.objects.all()
    serializer_class = UsersFriendsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'user_profile']
