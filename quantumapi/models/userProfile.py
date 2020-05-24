from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import cloudinary
# import cloudinary.uploader
# from cloudinary.api import delete_resources_by_tag, resources_by_tag
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url
from cloudinary.models import CloudinaryField
class UserProfile(models.Model):

    user = models.OneToOneField(User, unique=True, related_name="profile", null=True, on_delete=models.CASCADE, )
    address = models.CharField(null=True, blank=True, max_length=50,)
    picUrl = cloudinary.models.CloudinaryField('Image', overwrite=True, resource_type="image", transformation={"quality": "auto:eco"}, format="jpg",)
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
