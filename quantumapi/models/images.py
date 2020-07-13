import uuid
from django.db import models
from django.forms.widgets import ClearableFileInput
from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save




# def scramble_uploaded_filename(instance, filename):
#     extension = filename.split(".")[-1]
#     return "{}.{}".format(uuid.uuid4(), extension)

class Image(models.Model):
    image = models.ImageField(ClearableFileInput, upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.image.url

# @receiver(post_save, sender="quantumapi.UserProfile")
# def create_image(sender, instance, created, **kwargs):
#     if created:
#         Image.objects.create(image=instance)

# @receiver(post_save, sender="quantumapi.UserProfile")
# def save_image(sender, instance, **kwargs):
#     instance.image.save()



class ImageForm(forms.FileInput):
    class Meta:
        model = Image
        fields = ('image', )
