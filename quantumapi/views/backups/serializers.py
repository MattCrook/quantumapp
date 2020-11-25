# from rest_framework import serializers
# from quantumapi.models import User
# from rest_framework.serializers import ModelSerializer
# # from drf_queryfields import QueryFieldsMixin




# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         email=serializers.SerializerMethodField()
#         fields = ('id', 'url', 'email', 'first_name', 'last_name', 'password', 'username', 'last_login', 'is_staff', 'date_joined', 'groups', 'user_permissions', 'userprofile', )
#         # extra_kwargs = {'password': {'write_only': True}}
#         depth = 1

    # def create(self, validated_data):
    #     # password was .pop()...need the password for the DB...was loosing it at registration.
    #     password = validated_data.pop('password') 
    #     user = User(**validated_data)
    #     user.email = validated_data.get('email')
    #     user.set_password(password)
    #     user.save()
    #     print("USER", user)
    #     return user

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
    
    # def get_email(self, obj):
    #     return obj.email
