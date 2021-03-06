from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required, permission_required
from quantumapi.models import Credential, Messages
from quantumapi.models import UserProfile as UserProfileModel
from django.contrib.sessions.models import Session
from quantumforum.models import Friendships, FriendRequest, GroupChat, GroupMembersJoin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from social_django.context_processors import backends, user_backends_data
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_backends
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
import datetime
# from django.contrib.sessions.backends.db import SessionStore
# from social_django.context_processors import backends, user_backends_data





# @permission_required([IsAuthenticated])
# @authentication_classes([SessionAuthentication, TokenAuthentication, JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])

@login_required(redirect_field_name='login')
def group_chat_view(request):
    if request.method == 'GET':
        user = request.user
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        decoded_session_data = request.session.decode(session.session_data)
        UserModel = get_user_model()
        backend_list = get_backends()
        auth_user_backends = backends(request)

        user_profile = UserProfileModel.objects.get(user_id=user.id)
        all_users = UserModel.objects.all()
        default_profile_pic = "https://aesusdesign.com/wp-content/uploads/2019/06/mans-blank-profile-768x768.png"

        # Each join, get all that user has sent, and then all they received.
        sent_friendships = Friendships.objects.filter(requester_id=user.id)
        received_friendships = Friendships.objects.filter(addressee=user.id)
        accepted_sent_friendships = []
        accepted_sent_friend_requests = []
        accepted_received_friendships = []
        accepted_received_friend_requests = []
        quantum_friends = []
        active_friends = []
        group_chats = []

        # loop thru each join and get the friend request object.
        for f in sent_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_sent_friendships.append(f)
                    accepted_sent_friend_requests.append(friend_request)
                    addressee = UserModel.objects.get(pk=f.addressee_id)
                    quantum_friends.append(addressee)

        for f in received_friendships:
            friendship_id = f.id
            is_friend_request = FriendRequest.objects.filter(sender_and_receiver=friendship_id).exists()
            if is_friend_request:
                friend_request = FriendRequest.objects.get(sender_and_receiver=friendship_id)
                if friend_request.status_code.code == '1':
                    accepted_received_friendships.append(f)
                    accepted_received_friend_requests.append(friend_request)
                    requester = UserModel.objects.get(pk=f.requester_id)
                    quantum_friends.append(requester)

        for friend in quantum_friends:
            if friend.is_active == True:
                active_friends.append(friend)

        has_active_friends = len(active_friends) > 0

        user_assoc_group_chats = GroupMembersJoin.objects.filter(user_profile_id=user_profile.id)

        for group in user_assoc_group_chats:
            group_id = group.group_id
            group_chat = GroupChat.objects.get(pk=group_id)
            group_chats.append(group_chat)


        friend_data = {
            'accepted_sent_friendships': accepted_sent_friendships,
            'accepted_sent_friend_requests': accepted_sent_friend_requests,
            'accepted_received_friendships': accepted_received_friendships,
            'accepted_received_friend_requests': accepted_received_friend_requests,
            'active_friends': active_friends
        }

        template = 'group_chat/group_chat.html'
        context = {
            'user': user,
            'user_profile': user_profile,
            'all_users': all_users,
            'friend_data': friend_data,
            'quantum_friends': quantum_friends,
            'default_profile_pic': default_profile_pic,
            'has_active_friends': has_active_friends,
            'active_friends': active_friends,
            'group_chats': group_chats,
        }
        return render(request, template, context)

    if request.method == 'POST':
        try:
            form_data = request.POST
            group_name = request.POST.get('group_name')
            all_users_in_group = set()
            user = request.user
            user_profile = UserProfileModel.objects.get(user_id=user.id)
            participant_ids = []

            for p in form_data:
                if p.split("-")[0] == 'participant':
                    participant_ids.append(p.split("-")[1])

            for pid in participant_ids:
                group_member_user_profile = UserProfileModel.objects.get(pk=pid)
                all_users_in_group.add(group_member_user_profile)

            all_group_members = list(all_users_in_group)
            all_group_members.append(user_profile)

            new_group = GroupChat()
            new_group.name = group_name
            new_group.members = all_group_members
            new_group.created_by = user
            new_group.created_at = datetime.datetime.now()
            # new_group.is_valid()
            new_group.save()


            # Then loop through all of invited group members,
            # User who created group should be included in the array.
            for member in all_group_members:
                new_group_members_join = GroupMembersJoin()
                new_group_members_join.user_profile = member
                new_group_members_join.group = new_group
                new_group_members_join.save()

        except Exception as ex:
            HttpResponse(ex.args, content='application/json')

        return redirect(reverse('quantumforum:staging_room', kwargs={'group_id': new_group.id}))
