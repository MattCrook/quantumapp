from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from quantumforum.views import index, login_user, logout_user, group_chat, private_chat, room
from quantumforum.views import redirect_home as client_home
from quantumforum.views import redirect_profile as profile
from quantumforum.views import error as error_view




app_name = 'quantumforum'

urlpatterns = [
    # Hits the index first, index checks for login, if not redirects to login page, if so, redirects to requested page.
    # path('authenticate/<str:chat_type>/', index, name='index'),

    # Will render to default django login form - can't override - must be at registration/login
    # path('accounts', include('django.contrib.auth.urls')),
    # path('', include('django.contrib.auth.urls')),

    path('index/', index, name='index'),
    path('forum/login/', login_user, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('group_chat/', group_chat, name='group_chat'),
    # path('complete/auth0', complete, name='complete'),
    path('logout/', logout_user, name='logout'),
    path('home/', client_home, name='home'),
    path('user/profile/credits', profile, name='profile'),
    path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
    path('error', error_view, name='error'),

    # path('<str:room_name>/', room, name='room'),
    # path('private_chat/<int:auth_user_id>/', private_chat, name='private_chat'),
]
