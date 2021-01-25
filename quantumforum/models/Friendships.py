from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model




class Friendships(models.Model):
    UserModel = get_user_model()

    requester = models.ForeignKey("self", on_delete=models.CASCADE)
    addressee = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Friendship")
        verbose_name_plural = ("Friendships")
        unique_together = [("requester", "addressee")]

    def __str__(self):
        return f'Sent by: {self.requester.first_name} {self.requester.last_name}'
