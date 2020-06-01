from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tracktype(models.Model):

    name = models.CharField(max_length=50, null=True)


    class Meta:
        verbose_name = ("tracktype")
        verbose_name_plural = ("tracktypes")
        ordering = ("name",)


    def __str__(self):
        return f'{self.name}'
