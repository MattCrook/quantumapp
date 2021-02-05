from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# from quantumforum.models import GroupChat
from quantumapi.models import UserProfile


class GroupMembersJoin(models.Model):
    # UserModel = get_user_model()

    group = models.ForeignKey("GroupChat", null=True, blank=True, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Group Chat Join")
        verbose_name_plural = ("Group Chats Join")

    def __str__(self):
        return f'{self.group.group.name}'
