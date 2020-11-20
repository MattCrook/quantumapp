import json
from quantumapi.models import User
from quantumapi.models import Auth0Data as Auth0DataModel
from django.db import models


class Credential(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    auth0data = models.ForeignKey(Auth0DataModel, null=True, blank=True, on_delete=models.CASCADE)
    django_token = models.CharField(max_length=100, null=True, blank=True)
    django_session = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = ("credential")
        verbose_name_plural = ("credentials")
        ordering = ("user", )

    def __str__(self):
        return f'{self.user.username} -- {self.django_session}'
