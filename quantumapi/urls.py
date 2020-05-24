from django.urls import path, include
# from . import views
# from rest_framework.schemas import get_schema_view
from quantumapi.utils import jwt_decode_token, jwt_get_username_from_payload_handler




urlpatterns = [
    path('', include('jwt_decode_token')),
    path('', include('jwt_get_username_from_payload_handler')),

]


      # path('api/userprofile/', views.UserProfiles.as_view()),
      # path('api/rollercoaster/', views.RollerCoasters.as_view()),
      # path('api/manufacturer/', views.Manufacturers.as_view()),
      # path('api/tracktype/', views.Tracktypes.as_view()),
      # path('api/messages/', views.Message.as_view()),
      # path('api/park/', views.Parks.as_view()),
#     path('api/public', views.public),
#     path('api/private', views.private),
#     path('api/private-scoped', views.private_scoped),
