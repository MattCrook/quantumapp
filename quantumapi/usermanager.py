from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



# Creates and saves a User with the given email and password.
# Have to define custom UserManager. That’s because the existing manager define the create_user and create_superuser methods.
# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         return self.create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)


# class UserWithProfile(AbstractUser):

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.profile = UserProfile(user=self)
#         super(UserWithProfile, self).save(*args, **kwargs)


# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE, )
