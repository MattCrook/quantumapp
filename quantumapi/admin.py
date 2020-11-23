from django.contrib import admin
from quantumapi.models import UserProfile, RollerCoaster, Tracktype, Manufacturer, Park, Credit, Messages, Image, User, NewsArticle
from quantumapi.models import Credential as CredentialModel
from quantumapi.models import QuantumUserAdmin


admin.site.register(UserProfile)
admin.site.register(Tracktype)
admin.site.register(Manufacturer)
admin.site.register(Park)
admin.site.register(RollerCoaster)
admin.site.register(Credit)
admin.site.register(Messages)
admin.site.register(Image)
admin.site.register(User, QuantumUserAdmin)
admin.site.register(CredentialModel)
admin.site.register(NewsArticle)
