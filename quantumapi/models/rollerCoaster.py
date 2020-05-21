from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .manufacturer import Manufacturer
from .park import Park
from .trackType import Tracktype

class RollerCoaster(models.Model):

    name = models.CharField(max_length=50)
    tracktype = models.ForeignKey(Tracktype, related_name='rollercoasters', on_delete=models.CASCADE)
    max_height = models.CharField(max_length=50)
    max_speed = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, related_name='rollercoasters', on_delete=models.CASCADE)
    park = models.ForeignKey(Park, related_name='rollercoasters', on_delete=models.CASCADE)
    user_credit_id = models.ManyToManyField("UserProfile", through="Credit")

    class Meta:
        verbose_name = ("rollerCoaster")
        verbose_name_plural = ("rollerCoasters")
        ordering = ("manufacturer",)


    def __str__(self):
        return f'Name: {self.name}, Speed: {self.max_speed}, Height: {self.max_height}.'
