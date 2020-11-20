import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from quantumapi.models import User
from quantumapi.models import Auth0Data as Auth0DataModel
from quantumapi.models import Credential as CredentialModel


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialModel
        url = serializers.HyperlinkedIdentityField(
            view_name='credentials', lookup_field='id')
        fields = ('id', 'user', 'auth0data', 'django_token', 'django_session')
        depth = 1


class Credentials(ViewSet):

    def list(self, request):
        credentials_data = CredentialModel.objects.all()
        user_id = self.request.query_params.get("user_id", None)

        if user_id is not None:
            credentials_data = credentials_data.filter(user_id=user_id)
        serializer = CredentialsSerializer(
            credentials_data, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            if pk is not None:
                credentials = CredentialModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None)
            session = self.request.query_params.get("session", None)
            django_token = self.request.query_params.get("QuantumToken", None)
            auth0data = self.request.query_params.get("auth0data", None)

            if user_id is not None:
                credentials = CredentialModel.objects.filter(user_id=user_id)

            if session is not None:
                credentials = CredentialModel.objects.filter(session=session)

            if django_token is not None:
                credentials = CredentialModel.objects.filter(
                    django_token=django_token)

            if auth0data is not None:
                credentials = CredentialModel.objects.filter(
                    auth0data=auth0data)

            serializer = CredentialsSerializer(
                credentials, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        try:
            req_data = request.data
            session_key = request.session.session_key
            session = request.session

            if 'user_id' in request.data and request.data['user_id']:
                current_user = User.objects.get(pk=req_data['user_id'])
                is_credential = CredentialModel.objects.filter(user_id=current_user.id).exists()
                print("IS CRED", is_credential)
                if is_credential:
                    credential = CredentialModel.objects.get(user_id=current_user.id)
                    credential.user = current_user
                    credential.auth0data = Auth0DataModel.objects.get(user_id=current_user.id)
                    credential.django_token = req_data["django_token"]
                    credential.django_session = session_key
                    credential.save();
                    serializer = CredentialsSerializer(credential, context={'request': request})
                    return Response(serializer.data)
                else:
                    new_credentials = CredentialModel.objects.create(
                        user_id=current_user.id,
                        auth0data_id=req_data['auth0data_id'],
                        django_token=req_data['django_token'],
                        django_session=session_key)
                    print(new_credentials)
                    serializer = CredentialsSerializer(new_credentials, context={'request': request})
                    return Response(serializer.data)

            else:
                return HttpResponse(b'Error: Request error, User Id did not match current user Id or payload was empty.', content_type='application/json')
        except Exception as ex:
            print("EXEPTION", ex)
            return HttpResponse({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AssertionError as ass:
            return HttpResponse({'message': ass.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
