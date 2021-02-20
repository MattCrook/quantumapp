from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import Credential, Messages
from quantumapi.models import UserProfile as UserProfileModel
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated




@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def staging_room(request, group_id):
    if request.method == 'GET':
        auth_user = request.user
        user_profile = UserProfileModel.objects.get(user_id=auth_user.id)
        group = GroupChat.objects.get(pk=group_id)
        group_members_join = group.group_members
        group_participants = GroupMembersJoin.objects.filter(group_id=group_id)
        group_members = set()

        for member in group_participants:
            member_user_profile = UserProfileModel.objects.get(pk=member.user_profile_id)
            group_members.add(member_user_profile)

        group_members = list(group_members)
        template = 'group_chat/staging_room.html'
        context = {
            'group': group,
            'group_members_join': group_members_join,
            'group_members': group_members,
            'auth_user': auth_user,
            'user_profile': user_profile
        }

        return render(request, template, context)
