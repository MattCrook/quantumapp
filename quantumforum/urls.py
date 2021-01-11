from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import  include


urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
