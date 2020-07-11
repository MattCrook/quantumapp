from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .images import Image

# import cloudinary
# from cloudinary.models import CloudinaryField
# import cloudinary.uploader
# from cloudinary.api import delete_resources_by_tag, resources_by_tag
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url



class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name="profile", null=True, blank=True, on_delete=models.CASCADE, )
    address = models.CharField(null=True, blank=True, max_length=50,)
    image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE)
    rollerCoaster_id = models.ManyToManyField("RollerCoaster", through="Credit", )

    class Meta:
        verbose_name = ("userProfile")
        verbose_name_plural = ("userProfiles")

    def __str__(self):
          return f'Name: {self.user.first_name} {self.user.last_name} -- Username: {self.user.username} -- Email: {self.user.email} -- Address: {self.address} -- Credits:{self.rollerCoaster_id}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
