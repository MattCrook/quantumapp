from django.urls import path
from quantumadminapp.views import index

app_name = 'quantumadminapp'

urlpatterns = [
    path('quantumadmin/', index, name='index'),
]
