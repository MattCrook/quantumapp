from rest_framework.authentication import authenticate, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from quantumforum.models import GroupChat as GroupChatModel
from django_filters.rest_framework import DjangoFilterBackend
import datetime


class GroupChatSerializer(serializers.ModelSerializer):
        class Meta:
            model = GroupChatModel
            fields = ('id', 'name', 'group_members', 'created_at', 'created_by_id')
            depth = 2



class GroupChatApiView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = GroupChatModel.objects.all()
    serializer_class = GroupChatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'created_by_id']
