from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .userProfile import UserProfile
# from .rollerCoaster import RollerCoaster


class Credit(models.Model):

    rollerCoaster = models.ForeignKey("RollerCoaster", related_name="credits", on_delete=models.CASCADE, )
    userProfile = models.ForeignKey("UserProfile", related_name="users", on_delete=models.CASCADE, )


    class Meta:
        verbose_name = ("credit")
        verbose_name_plural = ("credits")
        # ordering = (F('user.date_joined').asc(nulls_last=True),)


    def __str__(self):
        return f'{self.userProfile.user.first_name} {self.userProfile.user.last_name} - {self.rollerCoaster.name} - {self.rollerCoaster.park.name}'
