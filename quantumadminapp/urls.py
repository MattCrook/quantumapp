from django.urls import path
from quantumadminapp.views import index, login_admin_user, register_admin_user
from django.conf.urls.static import static
from quantumapp import settings


app_name = 'quantumadminapp'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_admin_user, name='login_admin_user'),
    path('register/', register_admin_user, name='register_admin_user'),
]
#  + static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
