from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from quantumapi.models import UserProfile as UserProfileModel
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from social_django.context_processors import backends, user_backends_data
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_backends
# from social_django.context_processors import backends
# from django.contrib.sessions.backends.db import SessionStore
# from django.contrib.sessions.models import Session


@authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def edit_group_chat_form(request, group_id):
    if request.method == 'GET':
        auth_user = request.user
        default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"
        group = GroupChat.objects.get(pk=group_id)
        sent_friendships = Friendships.objects.filter(requester_id=auth_user.id)
        received_friendships = Friendships.objects.filter(addressee=auth_user.id)
        UserModel = get_user_model()
        user_profile = UserProfileModel.objects.get(user_id=auth_user.id)
        group_members = GroupMembersJoin.objects.filter(group_id=group_id)
        quantum_friends = []
        accepted_sent_friend_requests = []
        accepted_received_friend_requests = []
        created_by_fullname = group.created_by.get_full_name()


        for f in sent_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_sent_friend_requests.append(friend_request)
                    addressee = UserModel.objects.get(pk=f.addressee_id)
                    quantum_friends.append(addressee)

        for f in received_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_received_friend_requests.append(friend_request)
                    requester = UserModel.objects.get(pk=f.requester_id)
                    quantum_friends.append(requester)


        template = 'group_chat/group_chat_edit_form.html'
        context = {
            'group': group,
            'auth_user': auth_user,
            'user_profile': user_profile,
            'group_members': group_members,
            'quantum_friends': quantum_friends,
            'created_by_fullname': created_by_fullname,
            'default_profile_pic': default_profile_pic
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        if ("actual_method" in form_data and form_data["actual_method"] == "PUT"):
            group = GroupChat.objects.get(pk=group_id)
