from django.urls import path
from . import views
from .auth import forum_login as forum_login_view
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from .models.forms import LoginForm



app_name = "quantumforum"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('accounts/login/', forum_login_view, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=LoginForm)),
    # path('api-token-auth/', obtain_auth_token),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    path('authenticate_for_group_chat/<int:auth_user_id>/', views.authenticate_for_group_chat, name="authenticate_for_group_chat"),
    path('group_chat/', views.group_chat, name='group_chat'),
    path('private_chat/<int:auth_user_id>/', views.private_chat, name='private_chat'),
    path('<str:room_name>/', views.room, name='room'),
]
