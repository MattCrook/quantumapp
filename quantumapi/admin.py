from django.contrib import admin
from quantumapi.models import UserProfile, RollerCoaster, Tracktype, Manufacturer, Park
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Tracktype)
admin.site.register(Manufacturer)
admin.site.register(Park)
admin.site.register(RollerCoaster)
