from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import User as UserModel
from quantumapi.models import LoginHistory as LoginHistoryModel
import socket
import os


class LoginInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistoryModel
        url = serializers.HyperlinkedIdentityField(view_name='loginhistory', lookup_field='id')
        fields = ('id', 'user', 'email', 'recent_attempts', 'ip_address', 'browser', 'version', 'platform', 'app_codename', 'host_computer_name', 'total_logins', 'date')
        depth = 1




class LoginInfoView(ViewSet):

    def list(self, request):
        data = LoginHistoryModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = LoginHistoryModel.objects.filter(user_id=user_id)

        serializer = LoginInfoSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            data = LoginHistoryModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);
            if user_id is not None:
                data = LoginHistoryModel.objects.filter(user_id=user_id)

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
            print(ipv4s[-1])
            print(host_ip)
            print(IPAddr)

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

            login_info.save()
            serializer = LoginInfoSerializer(login_info, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None):
        try:
            login_info = LoginHistoryModel.objects.get(pk=pk)
            login_info.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except LoginHistoryModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
