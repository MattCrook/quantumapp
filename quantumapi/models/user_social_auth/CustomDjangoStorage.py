from django.db import models
from social_django.models import AbstractUserSocialAuth, DjangoStorage, UserSocialAuth
# from quantumapp.settings import AUTH_USER_MODEL

# class CustomUserSocialAuth(AbstractUserSocialAuth):
#     user = models.ForeignKey(AUTH_USER_MODEL, related_name='custom_social_auth', on_delete=models.CASCADE)


class CustomDjangoStorage(DjangoStorage):
    user = UserSocialAuth
