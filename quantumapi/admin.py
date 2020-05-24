from django.contrib import admin
from quantumapi.models import UserProfile, RollerCoaster, Tracktype, Manufacturer, Park, Credit

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register models here.

admin.site.register(UserProfile)
admin.site.register(Tracktype)
admin.site.register(Manufacturer)
admin.site.register(Park)
admin.site.register(RollerCoaster)
admin.site.register(Credit)


# User = get_user_model()

# @admin.register(User)
# class UserAdmin(UserAdmin):
#     pass
