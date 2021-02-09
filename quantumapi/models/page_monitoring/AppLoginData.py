import json
from quantumapi.models import User as UserModel
from social_django.models import UserSocialAuth
from django.db import models
from django.utils import timezone


class AppLoginData(models.Model):
    auth_user = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, null=True, blank=True)
    management_api_user = models.TextField(null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    management_api_token = models.TextField(null=True, blank=True)
    rest_auth_token = models.TextField(null=True, blank=True)
    strategy = models.CharField(max_length=50, blank=True, null=True)
    strategy_type = models.CharField(max_length=50, blank=True, null=True)
    prompts = models.TextField(null=True, blank=True)
    recent_attempts = models.CharField(max_length=2, null=True, blank=True)
    total_logins = models.CharField(max_length=6, null=True, blank=True, default=0)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True, blank=True)
    oauth_endpoint_scopes = models.TextField(null=True, blank=True)
    openid_configuration = models.TextField(null=True, blank=True)
    grants = models.TextField(null=True, blank=True)
    client_grants = models.TextField(null=True, blank=True)
    connections = models.TextField(null=True, blank=True)
    user_logs = models.TextField(null=True, blank=True)
    resource_servers = models.TextField(null=True, blank=True)
    management_api_keys = models.TextField(null=True, blank=True)
    device_credentials = models.TextField(null=True, blank=True)
    rest_auth_session = models.TextField(null=True, blank=True)
    management_session_id = models.TextField(null=True, blank=True)
    management_session_user = models.CharField(max_length=100, blank=True, null=True)
    connection = models.TextField(null=True, blank=True)
    connection_id = models.TextField(null=True, blank=True)
    location_info = models.TextField(null=True, blank=True)
    last_login_ip = models.TextField(null=True, blank=True)
    social_user = models.ForeignKey(UserSocialAuth, null=True, blank=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=40, null=True, blank=True)
    updated_at = models.DateTimeField()


    class Meta:
        verbose_name = ("app Login Data")
        verbose_name_plural = ("app Login Data")
        ordering = ("auth_user", )

    def __str__(self):
        return f'{self.user.username} -- {self.recent_attempts} -- {self.date}'
