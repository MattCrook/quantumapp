from django.db import models
from django.urls import reverse
from quantumapi.models import UserProfile
from django.contrib.auth import get_user_model
from quantumforum.models import FriendRequest, FriendsJoin
from django.db.models.signals import post_save
from django.dispatch import receiver


UserModel = get_user_model()

class UsersFriends(models.Model):
    user_profile = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("FriendRequest", through="FriendsJoin", )

    class Meta:
        verbose_name = ("UserFriend")
        verbose_name_plural = ("UsersFriends")


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


# @receiver(post_save, sender=FriendsJoin)
# def create_users_friends(sender, instance, created, **kwargs):
#     if created:
#         UsersFriends.objects.create(friends=instance)

# @receiver(post_save, sender=FriendsJoin)
# def save_users_friends(sender, instance, **kwargs):
#     instance.friends.save()
