from django.db import models
from django.db.models import F
from .userProfile import UserProfile


class Messages(models.Model):

    message = models.CharField(max_length=50)
    timestamp = models.DateField(null=True)
    user = models.ForeignKey(
        UserProfile,
        null=True,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("message")
        verbose_name_plural = ("messages")
        ordering = ("timestamp",)


    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.last_name}: {self.message} ({self.timestamp})'
