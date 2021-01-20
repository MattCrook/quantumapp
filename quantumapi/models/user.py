from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .usermanager import CustomUserManager



class User(AbstractUser):
    first_name = models.CharField(('first name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(('last name'), max_length=50, blank=True)
    username = models.CharField(('username'), max_length=50, blank=True, null=True)
    email = models.CharField(('email'), max_length=50, blank=True)
    password = models.CharField(('password'), max_length=500, unique=True)
    auth0_identifier = models.CharField(('auth0_identifier'), max_length=150, unique=True)


    # USERNAME_FIELD = A string describing the name of the field on the User model that is used as the unique identifier.
    # The field must be unique (i.e., have unique=True set in its definition);
    # REQUIRED_FIELD =  A list of the field names that will be prompted for when creating a user via the createsuperuser management command;

    USERNAME_FIELD = 'auth0_identifier'
    REQUIRED_FIELDS = ['email', 'username', 'first_name', 'last_name']


    # Specifiesthat all objects for the class come from the CustomUserManager
    objects = CustomUserManager()


    def __str__(self):
        return "{}".format(self.email)
