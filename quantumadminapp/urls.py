from django.urls import path
from quantumadminapp.views import index
from django.conf.urls.static import static
from quantumapp import settings


app_name = 'quantumadminapp'

urlpatterns = [
    # path('quantumadmin/', index, name='index'),
    path('', index),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
