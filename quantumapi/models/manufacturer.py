from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Manufacturer(models.Model):

    name = models.CharField(max_length=50)
    origin_country = models.CharField(max_length=50)
    company_website = models.CharField(null=True, blank=True, max_length=50)


    class Meta:
        verbose_name = ("manufacturer")
        verbose_name_plural = ("manufacturers")
        ordering = ("name",)


    def __str__(self):
        return f'{self.name} -- {self.origin_country} -- {self.company_website}'
