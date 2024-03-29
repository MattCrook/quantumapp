from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
# from django.http import HttpResponse, HttpResponseServerError
from quantumapi.models import AppLoginData as AppLoginDataModel
# from quantumapi.views import UserSerializer
from rest_auth.models import TokenModel
# from social_django.models import UserSocialAuth

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# from rest_framework.authentication import RemoteUserAuthentication, TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from quantumapp.settings import AUTH0_DOMAIN
from quantumapi.views.auth.management_api_services import get_management_api_user, get_open_id_config, management_api_oath_endpoint, get_management_api_grants, get_management_api_client_grants, get_management_api_connections, retrieve_user_logs, resource_servers, management_api_keys, device_credentials, management_tenant_settings
# from django.contrib.auth import get_user_model
import datetime
import socket
# import os
import json





class AppLoginDataSerializer(serializers.Serializer):

    id = serializers.IntegerField(label='ID')
    auth_user = serializers.DictField()
    email = serializers.EmailField()
    management_api_user = serializers.DictField()
    access_token = serializers.CharField()
    management_api_token = serializers.CharField()
    rest_auth_token = serializers.CharField()
    strategy = serializers.CharField()
    strategy_type = serializers.CharField()
    prompts = serializers.DictField()
    recent_attempts = serializers.IntegerField()
    total_logins = serializers.IntegerField()
    ip_address = serializers.IPAddressField(protocol='both')
    oauth_endpoint_scopes = serializers.CharField()
    openid_configuration = serializers.DictField()
    grants = serializers.DictField()
    client_grants = serializers.DictField()
    connections = serializers.DictField()
    user_logs = serializers.DictField()
    resource_servers = serializers.DictField()
    management_api_keys = serializers.DictField()
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
    tenant_settings = serializers.DictField()
    updated_at = serializers.DateTimeField()



    # def create(self, validated_data):
    #     return AppLoginDataModel.objects.create(**validated_data)

    class Meta:
        model = AppLoginDataModel
        fields = ('id', 'auth_user', 'email', 'management_api_user', 'access_token', 'management_api_token', 'rest_auth_token', 'strategy', 'strategy_type', 'prompts', 'recent_attempts', 'total_logins', 'ip_address', 'oauth_endpoint_scopes', 'openid_configuration', 'grants', 'client_grants', 'connections', 'user_logs', 'resource_servers', 'management_api_keys', 'device_credentials', 'rest_auth_session', 'management_session_id', 'management_session_user', 'connection', 'connection_id', 'location_info', 'last_login_ip', 'social_user', 'client_name', 'tenant_settings', 'updated_at')
        depth = 1


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
                user_social_to_dict = {
                    "id": instance.social_user.id,
                    "uid": instance.social_user.uid,
                    "provider": instance.social_user.provider,
                    "user_id": instance.social_user.user_id,
                    "extra_data": instance.social_user.extra_data
                }
                data = {
                    'id': instance.id,
                    'auth_user': instance.auth_user.to_dict(),
                    'email': instance.auth_user.email,
                    'management_api_user': json.loads(instance.management_api_user),
                    'access_token': instance.access_token,
                    'management_api_token': instance.management_api_token,
                    'rest_auth_token': instance.rest_auth_token,
                    'strategy': instance.strategy,
                    'strategy_type': instance.strategy_type,
                    'prompts': json.loads(instance.prompts),
                    'recent_attempts': instance.recent_attempts,
                    'total_logins': instance.total_logins,
                    'ip_address': instance.ip_address,
                    'oauth_endpoint_scopes': instance.oauth_endpoint_scopes,
                    'openid_configuration': json.loads(instance.openid_configuration),
                    'grants': json.loads(instance.grants),
                    'client_grants': json.loads(instance.client_grants),
                    'connections': json.loads(instance.connections),
                    'user_logs': json.loads(instance.user_logs),
                    'resource_servers': json.loads(instance.resource_servers),
                    'management_api_keys': json.loads(instance.management_api_keys),
                    'device_credentials': instance.device_credentials,
                    'rest_auth_session': instance.rest_auth_session,
                    'management_session_id': instance.management_session_id,
                    'management_session_user': instance.management_session_user,
                    'connection': instance.connection,
                    'connection_id': instance.connection_id,
                    'location_info': json.loads(instance.location_info),
                    'last_login_ip': instance.last_login_ip,
                    'social_user': user_social_to_dict,
                    'client_name': instance.client_name,
                    'tenant_settings': instance.tenant_settings,
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
            tenant_settings = management_tenant_settings(AUTH0_DOMAIN, token)

            success_logins = [l for l in all_user_logs if l['type'] == 's']
            # success_exchange_authorization_codes = [l for l in all_user_logs if l['type'] == 'seacft']
            # success_logouts = [l for l in all_user_logs if l['type'] == 'slo']
            # success_exchange_authorization_code = success_exchange_authorization_codes[0]
            success_silent_authentications = [l for l in all_user_logs if l['type'] == 'ssa']
            success_login = success_logins[0]
            latest_success_silent_authentication = success_silent_authentications[0] if len(success_silent_authentications) > 0 else success_login

            # login_exchange_details = success_exchange_authorization_code.get('details')
            # login_exchange_code = login_exchange_details.get('code')
            scopes = serialized_management_api_token.get('scope')
            connection = success_login.get('connection')
            # log_date = success_login.get('date')
            connection_id = success_login.get('connection_id')
            client_name = success_login.get('client_name')
            log_ip = success_login.get('ip')
            location_info = success_login.get('location_info')
            management_session = success_login['details']['session_id']
            # management_user_id = success_login.get('user_id')
            # last_logout_ip = success_logouts[0].get('ip') if len(success_logouts) > 0 else management_user.get('last_ip')
            last_ip = management_user.get('last_ip')
            strategy = success_login.get('strategy')
            strategy_type = success_login.get('strategy_type')
            prompts = success_login['details']['prompts'] if len(success_login['details']['prompts']) > 0 else {}
            # management_session_user = prompts[0].get('session_user') if len(prompts) > 1 else latest_success_silent_authentication.get('details')['session_id']
            management_session_user = success_login['details']['session_id'] if len(prompts) > 1 else latest_success_silent_authentication.get('details')['session_id']
            rest_auth_token = TokenModel.objects.get(user=auth_user) if request.user else ""
            user_social_auth = auth_user.social_auth.get(user_id=auth_user.id)

            new_app_login_data = AppLoginDataModel.objects.create(
                auth_user=auth_user,
                email=auth_user.email,
                management_api_user=json.dumps(management_user),
                access_token=auth_token,
                management_api_token=token,
                rest_auth_token=rest_auth_token.key,
                strategy=strategy,
                strategy_type=strategy_type,
                prompts=json.dumps({"all_prompts": prompts}),
                recent_attempts=request.data['recent_attempts'],
                total_logins=management_user.get('logins_count'),
                ip_address=latest_success_silent_authentication.get('ip'),
                oauth_endpoint_scopes=scopes,
                openid_configuration=json.dumps(open_id_config),
                grants=json.dumps({"all_grants": grants}),
                client_grants=json.dumps({"all_client_grants": client_grants}),
                connections=json.dumps({"all_connections": connections}),
                user_logs=json.dumps({"all_user_logs": all_user_logs}),
                resource_servers=json.dumps({"all_resource_servers": management_resource_servers}),
                management_api_keys=json.dumps({"all_management_api_keys": api_keys}),
                device_credentials=device,
                rest_auth_session=request.data['sessionId'],
                management_session_id=management_session,
                management_session_user=management_session_user,
                connection=connection,
                connection_id=connection_id,
                location_info=json.dumps(location_info),
                last_login_ip=last_ip,
                social_user=user_social_auth,
                client_name=client_name,
                tenant_settings=tenant_settings,
                updated_at=datetime.datetime.now(),
            )

            social_user_dict = {
                "id": user_social_auth.id,
                "uid": user_social_auth.uid,
                "provider": user_social_auth.provider,
                "user_id": user_social_auth.user_id,
                "extra_data": user_social_auth.extra_data
            }

            data = {
                'id': new_app_login_data.id,
                'auth_user': auth_user.to_dict(),
                'email': auth_user.email,
                'management_api_user': management_user,
                'access_token': auth_token,
                'management_api_token': token,
                'rest_auth_token': rest_auth_token.key,
                'strategy': strategy,
                'strategy_type': strategy_type,
                'prompts': {"all_prompts": prompts},
                'recent_attempts': request.data['recent_attempts'],
                'total_logins': management_user.get('logins_count'),
                'ip_address': log_ip,
                'oauth_endpoint_scopes': scopes,
                'openid_configuration': open_id_config,
                'grants': {"all_grants": grants},
                'client_grants': {"all_client_grants": client_grants},
                'connections': {"all_connections": connections},
                'user_logs': {"all_user_logs": all_user_logs},
                'resource_servers': {"all_resource_servers": management_resource_servers},
                'management_api_keys': {"all_management_api_keys": api_keys},
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
                'tenant_settings': tenant_settings,
                'updated_at': datetime.datetime.now(),
            }


            serializer = AppLoginDataSerializer(data=data, context={'request': request})
            valid = serializer.is_valid()
            if valid:
                # AppLoginDataModel.objects.create(serializer.validated_data)
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
