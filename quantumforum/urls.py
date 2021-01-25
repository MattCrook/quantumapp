from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from quantumforum.views import index, login_user, logout_user, authenticate_for_group_chat, group_chat, private_chat, room




app_name = 'quantumforum'

urlpatterns = [
    # Hits the index first, index checks for login, if not redirects to login page, if so, redirects to requested page. 
    # path('authenticate/<str:chat_type>/', index, name='index'),

    # Will render to default django login form - can't override - must be at registration/login
    # path('accounts', include('django.contrib.auth.urls')),
    # path('', include('django.contrib.auth.urls')),

    path('login/', login_user, name='login'),
    path('logout', logout_user, name='logout'),

    path('social-auth/', include('social_django.urls', namespace='social')),
    path('authenticate_for_group_chat/<int:auth_user_id>/', authenticate_for_group_chat, name='authenticate_for_group_chat'),
    path('group_chat/', group_chat, name='group_chat'),
    path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    # path('<str:room_name>/', room, name='room'),

    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),



]
