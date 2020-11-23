import json
from quantumapi.models import User
from django.db import models


class Credential(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    user_sub = models.CharField(max_length=50, null=True, blank=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    client_id = models.CharField(max_length=100, null=True, blank=True)
    redirect_uri = models.CharField(max_length=100, null=True, blank=True)
    audience = models.CharField(max_length=150, null=True, blank=True)
    scope = models.CharField(max_length=100, null=True, blank=True)
    transactions = models.CharField(max_length=100, null=True, blank=True)
    nonce = models.CharField(max_length=100, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    django_token = models.CharField(max_length=100, null=True, blank=True)
    quantum_session = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = ("credential")
        verbose_name_plural = ("credentials")
        ordering = ("user", )

    def __str__(self):
        return f'{self.user.username} -- {self.user_sub} -- {self.quantum_session}'
