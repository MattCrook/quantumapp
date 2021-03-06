import json
from quantumapi.models import User as UserModel
from django.db import models
from django.utils import timezone


class ActivityLog(models.Model):
    user = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.CASCADE)
    action = models.TextField(null=True, blank=True, default=[])
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = ("Activity Log")
        verbose_name_plural = ("Activity Logs")
        ordering = ["date"]

    def __str__(self):
        return f'{self.user.username} -- {self.action} -- {self.date}'
