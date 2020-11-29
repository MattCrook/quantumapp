from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from quantumapp.settings import AUTH_USER_MODEL



# Creates and saves a User with the given email and password.
# Have to define custom UserManager. That’s because the existing manager define the create_user and create_superuser methods.
# Because we are using abstract user, have to define UserManager to use
# The create_user is invoked when doing a createsuperuser... **extra fields points to extra REQUIRED_FIELDS you add on user model.


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    User = AUTH_USER_MODEL

    def create_user(self, request, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password1=validated_data['password1'],
            password2=validated_data['password2'],
            auth0_identifier=validated_data['auth0_identifier'],
            address=validated_data['profile']['address']
        )

    # Create and save a SuperUser with the given email and password.
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
