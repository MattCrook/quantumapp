from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, related_name="userProfile", null=True, on_delete=models.CASCADE, )
    address = models.CharField(null=True, blank=True, max_length=50)
    picUrl = models.ImageField(null=True, blank=True)
    rollerCoaster_id = models.ManyToManyField("RollerCoaster", through="Credit", )

    class Meta:
        verbose_name = ("userProfile")
        verbose_name_plural = ("userProfiles")
        # ordering = (F('user.date_joined').asc(nulls_last=True),)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.username} {self.user.email} {self.user.id} {self.rollerCoaster_id}'


    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.userProfile = UserProfile(user=self)
    #     super(UserProfile, self).save(*args, **kwargs)
    #     return UserProfile
