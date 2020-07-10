import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from quantumapi.models import UserProfile
# from quantumapi.views import UserProfileSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, HttpResponseServerError


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )

        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'username',
                  'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'profile', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("VAL", validated_data)
        profile_data = validated_data.pop('profile')
        print("profiledata", profile_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.address = profile_data.get('address', profile.address)
        profile.image = profile_data.get('image', profile.image)
        profile.save()

        return instance


class Users(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def retrieve(self, request, pk=None):
    #     try:
    #         user = User.objects.get(pk=pk)
    #         serializer = UserSerializer(user, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     user = User.objects.get(pk=pk)
    #     user.username = request.data["username"]
    #     # Changing passwords has been tabled:
    #     # it will require password hashing...
    #     # user.password = request.data["password"]
    #     user.first_name = request.data["first_name"]
    #     user.last_name = request.data["last_name"]
    #     user.email = request.data["email"]
    #     user.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def get_user(request):

    req_body = json.loads(request.body.decode())
    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        token = req_body['token']
        user = Token.objects.get(key=token).user
        userdict = {
            "first": user.first_name,
            "last": user.last_name,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "token": token
        }
        return HttpResponse(json.dumps(userdict), content_type='application/json')
