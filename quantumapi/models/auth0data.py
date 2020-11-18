import json
from .user import User
from django.db import models


class Auth0Data(models.Model):

    user = models.OneToOneField(User, related_name="user", null=True, blank=True, on_delete=models.CASCADE)
    domain = models.CharField(max_length=100, null=True, blank=True)
    client_id = models.CharField(max_length=100, null=True, blank=True)
    redirect_uri = models.CharField(max_length=100, null=True, blank=True)
    audience = models.CharField(max_length=150, null=True, blank=True)
    scope = models.CharField(max_length=100, null=True, blank=True)
    transactions = models.CharField(max_length=100, null=True, blank=True)
    nonce = models.CharField(max_length=100, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = ("auth0data")
        ordering = ("user", )

    def __str__(self):
        return f'{self.user} -- {self.client_id} -- {self.audience}'
