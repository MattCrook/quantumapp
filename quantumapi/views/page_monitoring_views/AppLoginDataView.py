from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import AppLoginData as AppLoginDataModel
from quantumapi.views import UserSerializer
from rest_auth.models import TokenModel
from social_django.models import UserSocialAuth

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from quantumapp.settings import AUTH0_DOMAIN
from quantumapi.views.auth.management_api_services import get_management_api_user, get_open_id_config, management_api_oath_endpoint, get_management_api_grants, get_management_api_client_grants, get_management_api_connections, retrieve_user_logs, resource_servers, management_api_keys, device_credentials
from django.contrib.auth import get_user_model
import datetime
import socket
import os
import json

# from django.forms.models import model_to_dict



class AppLoginDataSerializer(serializers.Serializer):

    auth_user = serializers.DictField()
    email = serializers.EmailField()
    management_api_user = serializers.DictField()
    access_token = serializers.CharField()
    management_api_token = serializers.CharField()
    rest_auth_token = serializers.CharField()
    strategy = serializers.CharField()
    strategy_type = serializers.CharField()
    prompts = serializers.ListField()
    recent_attempts = serializers.IntegerField()
    total_logins = serializers.IntegerField()
    ip_address = serializers.IPAddressField(protocol='both')
    oauth_endpoint_scopes = serializers.CharField()
    openid_configuration = serializers.DictField()
    grants = serializers.ListField()
    client_grants = serializers.ListField()
    connections = serializers.ListField()
    user_logs = serializers.ListField()
    resource_servers = serializers.ListField()
    management_api_keys = serializers.ListField()
    device_credentials = serializers.CharField()
    rest_auth_session = serializers.CharField()
    management_session_id = serializers.CharField()
    management_session_user = serializers.CharField()
    connection = serializers.CharField()
    connection_id = serializers.CharField()
    location_info = serializers.DictField()
    last_login_ip = serializers.IPAddressField(protocol='both')
    social_user = serializers.DictField()
    client_name = serializers.CharField()
    updated_at = serializers.DateTimeField()



    def create(self, validated_data):
        return AppLoginDataModel.objects.create(**validated_data)

    class Meta:
        model = AppLoginDataModel
        fields = ['id', 'auth_user', 'email', 'management_api_user', 'access_token', 'management_api_token', 'rest_auth_token', 'strategy', 'strategy_type', 'prompts', 'recent_attempts', 'total_logins', 'ip_address', 'oauth_endpoint_scopes', 'openid_configuration', 'grants', 'client_grants', 'connections', 'user_logs', 'resource_servers', 'management_api_keys', 'device_credentials', 'rest_auth_session', 'management_session_id', 'management_session_user', 'connection', 'connection_id', 'location_info', 'last_login_ip', 'social_user', 'client_name', 'updated_at']
        depth = 2


class AppLoginDataView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        try:
            all_app_data = AppLoginDataModel.objects.all()
            user_id = self.request.query_params.get("auth_user_id", None)

            if user_id is not None:
                all_app_data = all_app_data.filter(auth_user_id=user_id)

            app_data_queryset = []

            for instance in all_app_data:
                data = {
                    'auth_user': instance.auth_user.to_dict(),
                    'email': instance.auth_user.email,
                    'management_api_user': instance.management_user,
                    'access_token': instance.auth_token,
                    'management_api_token': instance.token,
                    'rest_auth_token': instance.rest_auth_token.key,
                    'strategy': instance.strategy,
                    'strategy_type': instance.strategy_type,
                    'prompts': instance.prompts,
                    'recent_attempts': instance.request.data['recent_attempts'],
                    'total_logins': instance.management_user.get('logins_count'),
                    'ip_address': instance.log_ip,
                    'oauth_endpoint_scopes': instance.scopes,
                    'openid_configuration': instance.open_id_config,
                    'grants': instance.grants,
                    'client_grants': instance.client_grants,
                    'connections': instance.connections,
                    'user_logs': instance.all_user_logs,
                    'resource_servers': instance.management_resource_servers,
                    'management_api_keys': instance.api_keys,
                    'device_credentials': instance.device,
                    'rest_auth_session': request.data['sessionId'],
                    'management_session_id': instance.management_session,
                    'management_session_user': instance.management_session_user,
                    'connection': instance.connection,
                    'connection_id': instance.connection_id,
                    'location_info': instance.location_info,
                    'last_login_ip': instance.last_ip,
                    'social_user': instance.social_user,
                    'client_name': instance.client_name,
                    'updated_at': datetime.datetime.now(),
                }
                serializer = AppLoginDataSerializer(data=data, context={'request': request})
                valid = serializer.is_valid()
                if valid:
                    app_data_queryset.append(serializer.data)
                else:
                    print(serializer.errors)

            serializer = AppLoginDataSerializer(app_data_queryset, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        try:
            data = AppLoginDataModel.objects.get(pk=pk)
            serializer = AppLoginDataSerializer(data, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AppLoginDataModel.DoesNotExist as dne:
            return Response({'message': dne.args}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        try:
            auth_user = request.user
            auth_token = request.auth
            device = socket.gethostname()


            oauth_endpoint = management_api_oath_endpoint(AUTH0_DOMAIN)
            serialized_management_api_token = json.loads(oauth_endpoint)
            token = serialized_management_api_token['access_token']

            management_user = get_management_api_user(AUTH0_DOMAIN, token, auth_user.auth0_identifier.replace(".", "|"))
            open_id_config = get_open_id_config(AUTH0_DOMAIN, token)
            grants = get_management_api_grants(AUTH0_DOMAIN, token)
            client_grants = get_management_api_client_grants(AUTH0_DOMAIN, token)
            connections = get_management_api_connections(AUTH0_DOMAIN, token)
            management_resource_servers = resource_servers(AUTH0_DOMAIN, token)
            api_keys = management_api_keys(AUTH0_DOMAIN, token)
            all_user_logs = retrieve_user_logs(AUTH0_DOMAIN, token, auth_user.auth0_identifier.replace(".", "|"))

            success_logins = [l for l in all_user_logs if l['type'] == 's']
            success_exchange_authorization_codes = [l for l in all_user_logs if l['type'] == 'seacft']
            success_logouts = [l for l in all_user_logs if l['type'] == 'slo']
            success_silent_authentications = [l for l in all_user_logs if l['type'] == 'ssa']
            success_login = success_logins[0]
            success_exchange_authorization_code = success_exchange_authorization_codes[0]
            login_exchange_details = success_exchange_authorization_code.get('details')
            login_exchange_code = login_exchange_details.get('code')

            scopes = serialized_management_api_token.get('scope')
            connection = success_login.get('connection')
            log_date = success_login.get('date')
            connection_id = success_login.get('connection_id')
            client_name = success_login.get('client_name')
            log_ip = success_login.get('ip')
            location_info = success_login.get('location_info')
            management_session = success_login['details']['session_id']
            management_user_id = success_login.get('user_id')

            last_logout_ip = success_logouts[0].get('ip') if len(success_logouts) > 0 else management_user.get('last_ip')
            last_ip = management_user.get('last_ip')
            strategy = success_login.get('strategy')
            strategy_type = success_login.get('strategy_type')
            prompts = success_login['details']['prompts'] if len(success_login['details']['prompts']) > 0 else {}
            management_session_user = prompts[0].get('session_user') if len(prompts)> 0 else ""
            rest_auth_token = TokenModel.objects.get(user=auth_user) if request.user else ""
            user_social_auth = auth_user.social_auth.get(user_id=auth_user.id)

            social_user_dict = {
                "id": user_social_auth.id,
                "uid": user_social_auth.uid,
                "provider": user_social_auth.provider,
                "user_id": user_social_auth.user_id,
                "extra_data": user_social_auth.extra_data
            }

            data = {
                'auth_user': auth_user.to_dict(),
                'email': auth_user.email,
                'management_api_user': management_user,
                'access_token': auth_token,
                'management_api_token': token,
                'rest_auth_token': rest_auth_token.key,
                'strategy': strategy,
                'strategy_type': strategy_type,
                'prompts': prompts,
                'recent_attempts': request.data['recent_attempts'],
                'total_logins': management_user.get('logins_count'),
                'ip_address': log_ip,
                'oauth_endpoint_scopes': scopes,
                'openid_configuration': open_id_config,
                'grants': grants,
                'client_grants': client_grants,
                'connections': connections,
                'user_logs': all_user_logs,
                'resource_servers': management_resource_servers,
                'management_api_keys': api_keys,
                'device_credentials': device,
                'rest_auth_session': request.data['sessionId'],
                'management_session_id': management_session,
                'management_session_user': management_session_user,
                'connection': connection,
                'connection_id': connection_id,
                'location_info': location_info,
                'last_login_ip': last_ip,
                'social_user': social_user_dict,
                'client_name': client_name,
                'updated_at': datetime.datetime.now(),
            }
 

            serializer = AppLoginDataSerializer(data=data, context={'request': request})
            valid = serializer.is_valid()
            if valid:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'Serializer Error': serializer.errors }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            return Response({'Error': ex.args }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        try:
            app_login_data = AppLoginDataModel.objects.get(pk=pk)
            app_login_data.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except AppLoginDataModel.DoesNotExist as ex:
            return Response({'message': ex.args}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







            # new_app_login_data = AppLoginDataModel()
            # new_app_login_data.user = auth_user
            # new_app_login_data.email = auth_user.email
            # new_app_login_data.management_api_user = management_user
            # new_app_login_data.access_token = auth_token
            # new_app_login_data.management_api_token = token
            # new_app_login_data.rest_auth_token = rest_auth_token.key
            # new_app_login_data.strategy = strategy
            # new_app_login_data.strategy_type = strategy_type
            # new_app_login_data.prompts = prompts
            # new_app_login_data.recent_attempts = request.data['recent_attempts']
            # new_app_login_data.total_logins = management_user.get('logins_count')
            # new_app_login_data.ip_address = log_ip
            # new_app_login_data.oauth_endpoint_scopes = scopes
            # new_app_login_data.openid_configuration = open_id_config
            # new_app_login_data.grants = grants
            # new_app_login_data.client_grants = client_grants
            # new_app_login_data.connections = connections
            # new_app_login_data.user_logs = all_user_logs
            # new_app_login_data.resource_servers = management_resource_servers
            # new_app_login_data.management_api_keys = api_keys
            # new_app_login_data.rest_auth_session = request.session.session_key
            # new_app_login_data.management_session_id = management_session
            # new_app_login_data.management_session_user = management_session_user
            # new_app_login_data.connection = connection
            # new_app_login_data.connection_id = connection_id
            # new_app_login_data.location_info = location_info
            # new_app_login_data.last_login_ip = last_ip
            # new_app_login_data.social_user_id = auth_user.social_auth.get(user_id=auth_user.id)
            # new_app_login_data.client_name = client_name
            # new_app_login_data.updated_at = datetime.datetime.now()
            # new_app_login_data.save()
