from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import LoginHistory as LoginHistoryModel
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import socket
import os
import json
import datetime


class LoginInfoSerializer(serializers.ModelSerializer):

    user = serializers.DictField()
    email = serializers.CharField()
    recent_attempts = serializers.IntegerField()
    total_logins = serializers.IntegerField()
    ip_address = serializers.IPAddressField()
    browser = serializers.CharField()
    version = serializers.CharField()
    platform = serializers.CharField()
    app_codename = serializers.CharField()
    host_computer_name = serializers.CharField()
    id_token = serializers.DictField()
    date = serializers.DateTimeField()

    class Meta:
        model = LoginHistoryModel
        fields = ('id', 'user', 'email', 'recent_attempts', 'ip_address', 'browser', 'version', 'platform', 'app_codename', 'host_computer_name', 'total_logins', 'id_token', 'date')
        depth = 1




class LoginInfoView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        data = LoginHistoryModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = LoginHistoryModel.objects.filter(user_id=user_id)

        queryset_data = []

        for instance in data:
            login_info_instance = {
                "user": instance.user.to_dict(),
                "email": instance.email,
                "recent_attempts": instance.recent_attempts,
                "total_logins": instance.total_logins,
                "ip_address": instance.ip_address,
                "browser": instance.browser,
                "version": instance.version,
                "platform": instance.platform,
                "app_codename": instance.app_codename,
                "host_computer_name": instance.host_computer_name,
                "id_token": json.loads(instance.id_token),
                "date": instance.date
            }
            serializer = LoginInfoSerializer(data=login_info_instance, context={'request': request})
            valid = serializer.is_valid()
            if valid:
                queryset_data.append(serializer.data)
            else:
                print(serializer.errors)

        serializer = LoginInfoSerializer(queryset_data, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            data = LoginHistoryModel.objects.get(pk=pk)
            serializer = LoginInfoSerializer(data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            hostname = socket.gethostname()
            ipv4s = socket.gethostbyname_ex(socket.gethostname())[-1]
            host_ip = socket.getfqdn()
            host_ipv4 = ipv4s[-1]
            IPAddr = socket.gethostbyname(hostname)

            successful_authenticator = request.successful_authenticator
            auth_header = successful_authenticator.authenticate_header(request)
            get_token_from_auth_header = successful_authenticator.get_token_from_authorization_header(auth_header)
            # token_from_cookies = successful_authenticator.get_token_from_cookies(COOKIES)
            # token_from_request = successful_authenticator.get_token_from_request()
            # user_from_token = successful_authenticator.authenticate_credentials()


            user_id = request.data['user_id']
            is_user = LoginHistoryModel.objects.filter(user_id=user_id).exists()

            if is_user:
                login_info = LoginHistoryModel.objects.get(user_id=user_id)
                logins = login_info.total_logins
                new_total_logins = int(logins) + 1
                logins = str(new_total_logins)

            else:
                login_info = LoginHistoryModel()
                new_total_logins = 1
                logins = str(new_total_logins)

            user = UserModel.objects.get(pk=request.data['user_id'])
            login_info.user = user
            login_info.email = request.data["email"]
            login_info.recent_attempts = request.data["recent_attempts"]
            login_info.total_logins = logins
            login_info.ip_address = ipv4s[-1]
            login_info.browser = request.data["browser"]
            login_info.version = request.data["version"]
            login_info.platform = request.data["platform"]
            login_info.app_codename = request.data["app_code_name"]
            login_info.host_computer_name = hostname
            login_info.id_token = json.dumps(request.data['id_token'])
            login_info.date = datetime.datetime.now()

            data = {
                "user": user.to_dict(),
                "email": request.data["email"],
                "recent_attempts": request.data["recent_attempts"],
                "total_logins": logins,
                "ip_address": ipv4s[-1],
                "browser": request.data["browser"],
                "version": request.data["version"],
                "platform": request.data["platform"],
                "app_codename": request.data["app_code_name"],
                "host_computer_name": hostname,
                "id_token": request.data['id_token'],
                "date": datetime.datetime.now()
            }
            serializer = LoginInfoSerializer(data=data, context={'request': request})
            valid = serializer.is_valid()
            if valid:
                login_info.save()
                return Response(serializer.data)
            else:
                return Response({'Serializer Error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            login_info = LoginHistoryModel.objects.get(pk=pk)
            login_info.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except LoginHistoryModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
