from django.shortcuts import render
from quantumapi.models import User
from rest_framework.response import Response
from quantumapi.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from quantumapi.permissions import IsLoggedIUserOrAdmin, IsAdminUser
from rest_framework.views import APIView
from quantumapi.auth0_views import get_token_auth_header, requires_scope

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedIUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsLoggedIUserOrAdmin]
        return [permission() for permission in permission_classes]
