from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .usermanager import CustomUserManager
from social_django.models import DjangoStorage



class User(AbstractUser):
    first_name = models.CharField(('first name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(('last name'), max_length=50, blank=True)
    username = models.CharField(('username'), max_length=50, blank=True, null=True)
    email = models.CharField(('email'), max_length=50, blank=True)
    password = models.CharField(('password'), max_length=500, blank=True, null=True)
    auth0_identifier = models.CharField(('auth0_identifier'), max_length=150, unique=True)


    # USERNAME_FIELD = A string describing the name of the field on the User model that is used as the unique identifier.
    # The field must be unique (i.e., have unique=True set in its definition);
    # REQUIRED_FIELD =  A list of the field names that will be prompted for when creating a user via the createsuperuser management command;

    USERNAME_FIELD = 'auth0_identifier'
    REQUIRED_FIELDS = ['email', 'username', 'first_name', 'last_name']


    # Specifiesthat all objects for the class come from the CustomUserManager
    objects = CustomUserManager()
    storage = DjangoStorage()



    def to_dict(self):
        data = {}
        data['id'] = self.id
        data['last_login'] = self.last_login
        data['is_superuser'] = self.is_superuser
        data['is_staff'] = self.is_staff
        data['is_active'] = self.is_active
        data['date_joined'] = self.date_joined
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['username'] = self.username
        data['email'] = self.email
        data['password'] = self.password
        data['auth0_identifier'] = self.auth0_identifier
        return data


    def get_user(self):
        data = {
            'id': self.id,
            'last_login': self.last_login,
            'is_superuser': self.is_superuser,
            'is_staff': self.is_staff,
            'is_active': self.is_active,
            'date_joined': self.date_joined,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'auth0_identifier': self.auth0_identifier,
        }
        return data


    @staticmethod
    def get_session_hash(session):
        hash_dict = {}
        session_data = session.get_decoded()

        if '_auth_user_hash' in session_data:
            hash_dict['_auth_user_hash'] = session_data['_auth_user_hash']

        if 'auth0_state' in session_data:
             hash_dict['auth0_state'] = session_data['auth0_state']

        return hash_dict


    def get_session_data(self, session):
        '''
        Gets the auth session and the session tied to instantiated object user. Requires
        current session to be passed in as param. get_session_hash() is static method on class.
        '''
        session_hash = self.get_session_hash(session)
        auth_session_hash = self.get_session_auth_hash()
        session_data = {
            'session': session_hash,
            'auth_session': auth_session_hash
        }
        return session_data

    def fullname(self):
        return self.get_full_name()

    def __str__(self):
        return f'{self.email}'
