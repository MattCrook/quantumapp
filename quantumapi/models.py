# from django.db import models
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import ugettext_lazy as _


# class User(AbstractUser):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(('email address'), unique=True)
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

#     def __str__(self):
#         return "{}".format(self.email)


# class UserWithProfile(AbstractUser):

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.profile = UserProfile(user=self)
#         super(UserWithProfile, self).save(*args, **kwargs)


# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE, )
