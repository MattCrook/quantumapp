from rest_framework import serializers
from quantumapi.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'password', 'username', 'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.email = validated_data.get('email')
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        profile = UserProfile(**validated_data)
        profile_data = validated_data
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        profile.address = profile_data.get('address', instance.address)
        profile.picUrl = profile_data.get('picUrl', instance.picUrl)
        profile.rollerCoaster_id = profile_data.get('rollerCoaster_id', instance.rollerCoaster_id)
        profile.save()
