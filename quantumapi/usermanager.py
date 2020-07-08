# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.base_user import BaseUserManager
# from quantumapi.models import UserProfile, User





# Creates and saves a User with the given email and password.
# Have to define custom UserManager. That’s because the existing manager define the create_user and create_superuser methods.
# class UserManager(BaseUserManager):
#     # use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         profile = Profile(
#             user=user,
#             is_premium_member=is_premium_member,
#             has_support_contract=has_support_contract
#         )
#         profile.save()
#         return user

#     def create(self, validated_data):
#         return User.objects.create(
#         username=validated_data['username'],
#         email=validated_data['email'],
#         is_premium_member=validated_data['profile']['is_premium_member'],
#         has_support_contract=validated_data['profile']['has_support_contract']
#     )

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
