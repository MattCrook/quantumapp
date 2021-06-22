from quantumadminapp.views import index, login_admin_user, register_admin_user, get_csrf_and_forward_to_login, logout_admin_user
from django.urls import path
from django.conf.urls.static import static
from quantumapp import settings
from django.views.decorators.csrf import csrf_exempt


app_name = 'quantumadminapp'

urlpatterns = [
    path('', index, name='index'),
    path('login/', index, name='index'),
    path('login/complete/', login_admin_user),
    path('register/', index, name='index'),
    path('register/complete/', register_admin_user),
    path('api/get_csrf_silently/', get_csrf_and_forward_to_login),
    path('admin_logout/', logout_admin_user),
    path('api-dashboard/', index, name='index'),

    # path('login/', login_admin_user, name='login_admin_user'),
    # path('admin_login/', login_admin_user, name='admin_login'),
    # path('register/', register_admin_user, name='register_admin_user'),
]
#  + static(settings.IMAGES_URL, document_root=settings.IMAGES_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
