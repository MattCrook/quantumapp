from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import  include


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    path('group_chat/<int:auth_user_id>/', views.group_chat, name='group_chat'),
    path('private_chat/<int:auth_user_id>/', views.private_chat, name='private_chat'),

    path('<str:room_name>/', views.room, name='room'),
]
