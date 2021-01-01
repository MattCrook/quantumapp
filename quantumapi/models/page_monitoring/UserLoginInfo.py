import json
from quantumapi.models import User as UserModel
from django.db import models
from django.utils import timezone


class LoginHistory(models.Model):
    user = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, null=True, blank=True)
    recent_attempts = models.CharField(max_length=2, null=True, blank=True)
    total_logins = models.CharField(max_length=6, null=True, blank=True, default=0)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True, blank=True)
    host_computer_name = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)
    platform = models.CharField(max_length=200, null=True, blank=True)
    app_codename = models.CharField(max_length=50, null=True, blank=True)
    id_token = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = ("login history")
        verbose_name_plural = ("login history")
        ordering = ("user", )

    def __str__(self):
        return f'{self.user.username} -- {self.recent_attempts} -- {self.date}'
