from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
import django.utils.timezone

# from django.contrib.auth.models import PermissionsMixin
# from .userProfile import UserProfile
# from quantumapi.usermanager import UserManager



class User(AbstractUser):
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(('email address'), unique=True)

    # USERNAME_FIELD = A string describing the name of the field on the User model that is used as the unique identifier.
    # The field must be unique (i.e., have unique=True set in its definition);
    # REQUIRED_FIELD =  A list of the field names that will be prompted for when creating a user via the createsuperuser management command;

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


    def __str__(self):
        return "{}".format(self.email)
