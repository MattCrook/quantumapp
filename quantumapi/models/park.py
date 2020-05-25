from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Park(models.Model):

    name = models.CharField(max_length=50)
    parkLocation = models.CharField(max_length=50)
    parkCountry = models.CharField(max_length=50)


    class Meta:
        verbose_name = ("park")
        verbose_name_plural = ("parks")
        ordering = ("parkCountry", )


    def __str__(self):
        return f'{self.name} -- {self.parkLocation} -- {self.parkCountry}'
