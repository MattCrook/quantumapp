from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from quantumforum.views import index, login_user, logout_user, group_chat_view, staging_room, edit_group_chat_form, private_chat_view, room
from quantumforum.views import redirect_home as client_home
from quantumforum.views import redirect_profile as profile
from quantumforum.views import error as error_view
from quantumapi.views.user import get_auth_user
from django.contrib.auth import get_user_model



app_name = 'quantumforum'

urlpatterns = [
    # Hits the index first, index checks for login, if not redirects to login page, if so, redirects to requested page.
    # path('authenticate/<str:chat_type>/', index, name='index'),

    # Will render to default django login form - can't override - must be at registration/login
    # path('accounts', include('django.contrib.auth.urls')),
    # path('', include('django.contrib.auth.urls')),

    path('index/', index, name='index'),
    path('forum/login/', login_user, name='login'),
    path('', include('social_django.urls', namespace='social')),
    path('group_chat/', group_chat_view, name='group_chat'),
    path('logout/', logout_user, name='logout'),
    path('home/', client_home, name='home'),
    path('user/profile/credits', profile, name='profile'),
    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    path('private_chat/', private_chat_view, name='private_chat'),
    path('group_chat/<int:group_id>/confirm/', staging_room, name='staging_room'),
    path('group_chat/<int:group_id>/edit/', edit_group_chat_form, name='edit_group_chat_form'),
    path('error', error_view, name='error'),
    path('get_auth_user/', get_auth_user),


    # path('<str:room_name>/', room, name='room'),
]
