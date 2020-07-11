# from django.shortcuts import render
# from quantumapi.models import User, UserProfile
# from rest_framework.response import Response
# from quantumapi.serializers import UserSerializer
# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from quantumapi.permissions import IsLoggedIUserOrAdmin, IsAdminUser
# from rest_framework.views import APIView
# from quantumapi.auth0_views import get_token_auth_header, requires_scope
# from django.http import HttpResponseServerError
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status

# from django.shortcuts import render, redirect, get_object_or_404

# from quantumapi.models.model_factory import model_factory
# from django.views.decorators.csrf import csrf_exempt


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['email']


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

    # @csrf_exempt
    # def create(self, validated_data):
    #     # password was .pop()...need the password for the DB...was loosing it at registration.
    #     password = validated_data.pop('password') 
    #     user = User(**validated_data)
    #     user.email = validated_data.get('email')
    #     user.set_password(password)
    #     user.save()
    #     print("USER", user)
    #     return user


    # def update(self, request, pk=None):
    #     print("REQUEST", request.data)
    #     user = User.objects.get(pk=pk)
    #     userprofile = UserProfile.objects.get(user=user)
    #     print("UP", userprofile)


    #     user.first_name = request.data["first_name"]
    #     user.last_name = request.data["last_name"]
    #     user.username = request.data["username"]
    #     user.userprofile = userprofile

    #     user.save()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)


#############################################




    # def update(self, instance, validated_data):
    #     print("INSTANCE", instance)
    #     print("VALIDATEDDATA", validated_data)
    #     profile = UserProfile(**validated_data)
    #     profile_data = validated_data
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.username = validated_data.get('username', instance.username)

    #     profile.address = profile_data.get('address', instance.address)
    #     profile.picUrl = profile_data.get('picUrl', instance.picUrl)
    #     profile.rollerCoaster_id = profile_data.get('credits', instance.rollerCoaster_id)
    #     # profile.user
    #     print("PROFILE", profile)
    #     profile.save()
