from django.db import models
from django.urls import reverse
from quantumapi.models import UserProfile
from django.contrib.auth import get_user_model
from quantumforum.models import FriendRequest

UserModel = get_user_model()

class UsersFriends(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Friendships")

    class Meta:
        verbose_name = ("Friend")
        verbose_name_plural = ("Friends")


    @staticmethod
    def get_validated_friends(self):
        received_friend_requests = []
        sent_friend_requests = []
        quantum_friends = []

        friendships = self.friends
        for friend in friendships:
            friend_request = FriendRequest.objects.filter(sender_and_receiver=friend.id)
            if friend_request.status_code.code == '1':
                    requester = UserModel.objects.get(pk=friend.requester_id)
                    addressee = UserModel.objects.get(pk=friend.addressee_id)
                    received_friend_requests.append(requester)
                    addressee.append(addressee)

        quantum_friends.extend(received_friend_requests, sent_friend_requests)
        return quantum_friends



    def get_all_friends(self):
        data = {}
        friends = get_validated_friends()
        data['user_profile'] = self.user_profile
        data['friendships'] = self.friends
        data['friends'] = friends
        return data



    def __str__(self):
        return f'{self.user_profile.user.email}'
