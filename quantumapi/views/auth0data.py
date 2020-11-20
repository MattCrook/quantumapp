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



class Auth0DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auth0DataModel
        url = serializers.HyperlinkedIdentityField(view_name='auth0data', lookup_field='id')
        fields = ('id', 'user_id', 'domain', 'client_id', 'redirect_uri', 'audience', 'scope', 'transactions', 'nonce', 'access_token', 'updated_at')
        depth = 1



class Auth0Data(ViewSet):
    def list(self, request):
        data = Auth0DataModel.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = data.filter(user_id=user_id)
        serializer = Auth0DataSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)



    def retrieve(self, request, pk=None):
        try:
            if pk is not None:
                auth0data = Auth0DataModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);

            if user_id is not None:
                auth0data = auth0data.filter(user_id=user_id)

            serializer = Auth0DataSerializer(auth0data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def create(self, request):
        try:
            if "user_sub" in request.data and request.data['user_sub']:
                user_sub = request.data['user_sub']
                user = User.objects.get(auth0_identifier=user_sub)
                is_auth0data = Auth0DataModel.objects.filter(user_id=user.id).exists()

                if is_auth0data:
                    auth0data = Auth0DataModel.objects.get(user_id=user.id)
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
                    auth0data.updated_at = request.data["updated_at"]
                    auth0data.save()
                    serializer = Auth0DataSerializer(auth0data, context={'request': request})
                    return Response(serializer.data)
                else:
                    newAuth0data = Auth0DataModel()
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
                    newAuth0data.updated_at = request.data["updated_at"]
                    newAuth0data.save()
                    serializer = Auth0DataSerializer(newAuth0data, context={'request': request})
                    return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
        except AssertionError as ass:
            return HttpResponse({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        try:
            if request.method == "PATCH":
                req_data = request.data
                print('REQDATA', req_data)
                current_user_id = req_data['user_id']
                current_auth0data_id = req_data['id']
                auth0data = Auth0DataModel.objects.get(pk=current_auth0data_id)

                if 'nonce' in req_data:
                    auth0data.nonce = req_data['nonce']

                if 'access_token' in req_data:
                    auth0data.access_token = req_data['access_token']

                if 'updated_at' in req_data:
                    auth0data.updated_at = req_data['updated_at']

                auth0data.save()
            return Response({"Success": "Data successfully updated"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
