from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from quantumforum.models import FriendRequest, UsersFriends
from django.db.models.signals import post_save
from django.dispatch import receiver



class FriendsJoin(models.Model):
    users_friends = models.ForeignKey("UsersFriends", blank=True, null=True, on_delete=models.CASCADE)
    friend_request = models.ForeignKey(FriendRequest, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Friend Join")
        verbose_name_plural = ("Friends Join")

    def __str__(self):
        return f'Last Updated By: {self.friend_request.last_updated_by.email}'


@receiver(post_save, sender=UsersFriends)
def create_friends(sender, instance, created, **kwargs):
    if created:
        FriendsJoin.objects.create(users_friends=instance)

@receiver(post_save, sender=UsersFriends)
def save_friends(sender, instance, **kwargs):
    instance.users_friends.save()
