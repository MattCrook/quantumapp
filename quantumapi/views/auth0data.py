import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from quantumapi.models import User
from quantumapi.models import Credential as CredentialModel
from django.middleware.csrf import get_token


from django.views.decorators.csrf import csrf_protect
# from quantumapi.models import Auth0Data as Auth0DataModel



class CredentialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CredentialModel
        url = serializers.HyperlinkedIdentityField(view_name='credentials', lookup_field='id')
        fields = ('id', 'user_id', 'domain', 'client_id', 'redirect_uri', 'audience', 'scope', 'transactions', 'nonce', 'access_token', 'django_token', 'session_id', 'session', 'updated_at')
        depth = 1



class Credentials(ViewSet):
    def list(self, request):
        data = CredentialModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = CredentialModel.objects.filter(user_id=user_id)

        serializer = CredentialsSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)



    def retrieve(self, request, pk=None):
        try:
            if pk is not None:
                auth0data = CredentialModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);

            if user_id is not None:
                auth0data = CredentialModel.objects.filter(user_id=user_id)

            serializer = CredentialsSerializer(auth0data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # @csrf_protect
    def create(self, request):
        try:
            if "user_sub" in request.data and request.data['user_sub']:
                user_sub = request.data['user_sub']
                session = request.session.keys()
                csrftoken = get_token(request)
                print(csrftoken)
                print("SESSION", session)
                print(request.user.is_authenticated)
                user = User.objects.get(auth0_identifier=user_sub)
                is_auth0data = CredentialModel.objects.filter(user_id=user.id).exists()

                if is_auth0data and user_sub == user.auth0_identifier:
                    auth0data = CredentialModel.objects.get(user_id=user.id)
                    auth0data.user = user
                    auth0data.user_sub = request.data['user_sub']
                    auth0data.domain = request.data["domain"]
                    auth0data.client_id = request.data["client_id"]
                    auth0data.redirect_uri = request.data["redirect_uri"]
                    auth0data.audience = request.data["audience"]
                    auth0data.scope = request.data["scope"]
                    auth0data.transactions = request.data["transactions"]
                    auth0data.nonce = request.data["nonce"]
                    auth0data.access_token = request.data["access_token"]
                    auth0data.django_token = request.data["django_token"]
                    auth0data.session = request.data["session"]
                    auth0data.session_id = request.data["session_id"]
                    auth0data.csrf_token = csrftoken
                    auth0data.updated_at = request.data["updated_at"]
                    auth0data.save()
                    serializer = CredentialsSerializer(auth0data, context={'request': request})
                    return Response(serializer.data)
                else:
                    newAuth0data = CredentialModel()
                    newAuth0data.user = user
                    newAuth0data.user_sub = request.data['user_sub']
                    newAuth0data.domain = request.data["domain"]
                    newAuth0data.client_id = request.data["client_id"]
                    newAuth0data.redirect_uri = request.data["redirect_uri"]
                    newAuth0data.audience = request.data["audience"]
                    newAuth0data.scope = request.data["scope"]
                    newAuth0data.transactions = request.data["transactions"]
                    newAuth0data.nonce = request.data["nonce"]
                    newAuth0data.access_token = request.data["access_token"]
                    newAuth0data.django_token = request.data["django_token"]
                    newAuth0data.session = request.data["session"]
                    newAuth0data.session_id = request.data["session_id"]
                    newAuth0data.csrf_token = csrftoken
                    newAuth0data.updated_at = request.data["updated_at"]
                    newAuth0data.save()
                    serializer = CredentialsSerializer(newAuth0data, context={'request': request})
                    return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
        except AssertionError as ass:
            return HttpResponse({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        try:
            if request.method == "PATCH":
                req_data = request.data
                print('Auth0Data: REQDATA', req_data)
                current_user_id = req_data['user_id']
                current_auth0data_id = req_data['id']
                auth0data = CredentialModel.objects.get(pk=current_auth0data_id)

                if 'nonce' in req_data:
                    auth0data.nonce = req_data['nonce']

                if 'access_token' in req_data:
                    auth0data.access_token = req_data['access_token']

                if 'updated_at' in req_data:
                    auth0data.updated_at = req_data['updated_at']

                if 'session' in req_data:
                    auth0data.quantum_session = req_data['session']

                if 'django_token' in req_data:
                    auth0data.django_token = req_data['django_token']

                auth0data.save()

            elif request.method == 'PUT':
                data = CredentialModel.objects.get(pk=pk)
                if 'django_token' in request.data:
                    data.django_token = request.data['django_token']

                data.save()
            return Response({"Success": "Data successfully updated"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
