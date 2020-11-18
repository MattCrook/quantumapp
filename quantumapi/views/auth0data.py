import json
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication, permissions
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from .user import User


class Auth0DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auth0Data
        url = serializers.HyperlinkedIdentityField(view_name='auth0data', lookup_field='id')
        fields = ('id', 'user', 'domain', 'client_id', 'redirect_uri', 'audience', 'scope', 'transactions', 'nonce', 'access_token', 'updated_at')
        depth = 2



class Auth0Data(ViewSet):
    def list(self, request):
        data = Auth0Data.objects.all()
        user_id = self.request.query_params.get("user_id", None);

        if user_id is not None:
            data = data.filter(user_id=user_id)
        serializer = Auth0DataSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            auth0data = Auth0Data.objects.get(pk=pk)
            user_id = self.request.query_params.get("user_id", None);

            if user_id is not None:
                auth0data = auth0data.filter(user_id=user_id)
            serializer = Auth0DataSerializer(auth0data, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def create(self, request):
        newAuth0data = Auth0Data()
        user = User.objects.get(pk=request.data["user_id"])

        newAuth0data.user = user
        newAuth0data.domain = request.data["domain"]
        newAuth0data.client_id = request.data["client_id"]
        newAuth0data.redirect_uri = request.data["redirect_uri"]
        newAuth0data.manufacturer = request.data["max_height"]
        newAuth0data.scope = request.data["scope"]
        newAuth0data.transactions = request.data["transactions"]
        newAuth0data.nonce = request.data["nonce"]
        newAuth0data.access_token = request.data["access_token"]
        newAuth0data.updated_at = request.data["updated_at"]

        newAuth0data.save()
        serializer = Auth0DataSerializer(newAuth0data, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        try:
            if request.method == "PATCH":
                req_data = json.loads(request.data)
                current_user_id = req_data['user_id']
                current_auth0data_id = req_data['id']
                auth0data = Auth0Data.objects.get(pk=current_auth0data_id)

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
