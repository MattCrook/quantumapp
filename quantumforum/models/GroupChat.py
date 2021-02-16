from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from quantumapi.models import UserProfile


UserModel = get_user_model()

class GroupChat(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    group_members = models.ManyToManyField(UserProfile, through="GroupMembersJoin",)
    created_by = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.CASCADE,)
    created_at = models.DateTimeField()

    class Meta:
        verbose_name = ("Group Chat")
        verbose_name_plural = ("Group Chats")
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} - Created by: {self.created_by.user.first_name} {self.created_by.user.last_name} - At: {self.created_at}'
