from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .userProfile import UserProfile
from .rollerCoaster import RollerCoaster


class Credit(models.Model):

    rollerCoaster = models.ForeignKey(RollerCoaster, on_delete=models.CASCADE)
    userProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("credit")
        verbose_name_plural = ("credits")
        ordering = (F('user.date_joined').asc(nulls_last=True),)


    def __str__(self):
        return f'{self.name}'
