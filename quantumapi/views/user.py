from django.shortcuts import render
from quantumapi.models import User
from rest_framework.response import Response
from quantumapi.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from quantumapi.permissions import IsLoggedIUserOrAdmin, IsAdminUser
from rest_framework.views import APIView
from quantumapi.auth0_views import get_token_auth_header, requires_scope
from django.http import HttpResponseServerError
from django_filters.rest_framework import DjangoFilterBackend


import sqlite3
import datetime
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from quantumapi.views.connection import Connection
from quantumapi.models.model_factory import model_factory


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email']


    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedIUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsLoggedIUserOrAdmin]
    #     return [permission() for permission in permission_classes]


    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)




#############################################


# def get_user(email):
#     with sqlite3.connect(Connection.db_path) as conn:
#         conn.row_factory = model_factory(User)
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#             SELECT *
#             FROM quantumapi_user u
#             WHERE u.email = ?
#         """, (email, ))
#         data = db_cursor.fetchone()
#         print("DATA", data)
#         return data


# def get_user_email(request, email):
#     if request.method == 'GET':
#         # to_string = str(email)
#         user_email = get_user(email)
#         # template = 'training_programs/training_program_details.html'
#         context = {
#             "request": request,
#             "user_email": user_email,
#         }
#         return Response(context)
