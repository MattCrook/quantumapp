from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, authentication
from rest_framework.serializers import Serializer, ModelField
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
from django.conf import settings
from quantumapi.models import Credential as CredentialModel
from django.middleware.csrf import get_token
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_jwt.blacklist.models import BlacklistedToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from quantumapp.settings import AUTH0_CLIENT_ID, AUTH0_DOMAIN, API_IDENTIFIER, SOCIAL_AUTH_AUTH0_KEY
from quantumapi.views import UserSerializer
from django.contrib.auth import get_user_model
import datetime
import psycopg2
import json



class CredentialsSerializer(serializers.ModelSerializer):
    UserModel = get_user_model()

    user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    user_sub = serializers.CharField()
    domain = serializers.CharField()
    client_id = serializers.CharField()
    redirect_uri = serializers.CharField()
    audience = serializers.CharField()
    scope = serializers.CharField()
    transactions = serializers.JSONField()
    codes = serializers.JSONField()
    nonce = serializers.CharField()
    access_token = serializers.CharField()
    django_token = serializers.CharField()
    session_id = serializers.CharField()
    session = serializers.JSONField()
    csrf_token = serializers.CharField()
    cookies = serializers.JSONField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = CredentialModel
        fields = ('id', 'user', 'user_sub', 'domain', 'client_id', 'redirect_uri', 'audience', 'scope', 'transactions', 'codes', 'nonce', 'access_token', 'django_token', 'session_id', 'session', 'csrf_token', 'cookies', 'updated_at')
        depth = 1



class Credentials(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]

    def list(self, request):
        try:
            # data = CredentialModel.objects.all()
            # user_id = self.request.query_params.get("user_id", None);

            # if user_id is not None:
            #     data = CredentialModel.objects.filter(user_id=user_id)

            # serializer = CredentialsSerializer(data, many=True, context={'request': request})
            # return Response(serializer.data)
            credentials_instance = CredentialModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);
            if user_id is not None:
                credentials_instance = credentials_instance.filter(user_id=user_id)

            credentials = {
                "id": credentials_instance.id,
                "user": credentials_instance.user,
                "user_sub": credentials_instance.user_sub,
                "domain": credentials_instance.API_IDENTIFIER,
                "client_id": credentials_instance.SOCIAL_AUTH_AUTH0_KEY,
                "redirect_uri": credentials_instance.redirect_uri,
                "audience": credentials_instance.audience,
                "scope": credentials_instance.scope,
                "transactions": credentials_instance.transactions,
                "codes": credentials_instance.codes,
                "nonce": credentials_instance.nonce,
                "access_token": credentials_instance.access_token,
                "django_token": credentials_instance.django_token,
                "session": credentials_instance.decoded_session,
                "session_id": credentials_instance.session_id,
                "csrf_token": credentials_instance.csrftoken,
                "cookies": credentials_instance.cookies,
                "updated_at": credentials_instance.updated_at,
            }

            serializer = CredentialsSerializer(instance=credentials_instance, data=credentials, many=True, context={'request': request})
            serializer.is_valid()
            return Response(serializer.data)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def retrieve(self, request, pk=None):
        try:
            credentials_instance = CredentialModel.objects.get(pk=pk)

            user_id = self.request.query_params.get("user_id", None);
            if user_id is not None:
                credentials_instance = credentials_instance.filter(user_id=user_id)

            credentials = {
                "id": credentials_instance.id,
                "user": credentials_instance.user,
                "user_sub": credentials_instance.user_sub,
                "domain": credentials_instance.API_IDENTIFIER,
                "client_id": credentials_instance.SOCIAL_AUTH_AUTH0_KEY,
                "redirect_uri": credentials_instance.redirect_uri,
                "audience": credentials_instance.audience,
                "scope": credentials_instance.scope,
                "transactions": credentials_instance.transactions,
                "codes": credentials_instance.codes,
                "nonce": credentials_instance.nonce,
                "access_token": credentials_instance.access_token,
                "django_token": credentials_instance.django_token,
                "session": credentials_instance.decoded_session,
                "session_id": credentials_instance.session_id,
                "csrf_token": credentials_instance.csrftoken,
                "cookies": credentials_instance.cookies,
                "updated_at": credentials_instance.updated_at,
            }

            serializer = CredentialsSerializer(instance=credentials_instance, data=credentials, context={'request': request})
            serializer.is_valid()
            return Response(serializer.data)
        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        try:
            if "user_sub" in request.data and request.data['user_sub']:
                user_sub = request.data['user_sub']

                if 'csrf_token' in request.data and request.data['csrf_token']:
                    csrftoken = request.data['csrf_token']
                else:
                    print('Created csrf token on backend - none was set.')
                    csrftoken = get_token(request)

                if 'session_id' in request.data and request.data['session_id']:
                    session_id = request.data['session_id']
                    session = Session.objects.get(session_key=session_id)
                    decoded_session = request.session.decode(session.session_data)

                elif request.session and 'session_key' in request.session:
                    session = Session.objects.get(session_key=request.session.session_key)
                    decoded_session = request.session.decode(session.session_data)

                else:
                    print("Session Error: No Session tied to user.")
                    session_id = ''
                    decoded_session = ''

                if 'transactions' in request.data and request.data['transactions']:
                    all_transactions = request.data['transactions']
                    transaction_items_keys = all_transactions['transactions'].keys()
                    transactions_values = all_transactions['transactions'].values()
                    transactions = []
                    codes = []

                    for t in transactions_values:
                        transactions.append(t)

                    for c in transaction_items_keys:
                        codes.append(c)

                else:
                    transactions = {}

                user = request.user
                has_credentials = CredentialModel.objects.filter(user_id=user.id).exists()

                if has_credentials and user_sub == user.auth0_identifier:
                    credential_instance = CredentialModel.objects.get(user_id=user.id)
                    credential_instance.user = user
                    credential_instance.user_sub = request.data['user_sub']
                    credential_instance.domain = API_IDENTIFIER
                    credential_instance.client_id = SOCIAL_AUTH_AUTH0_KEY
                    credential_instance.redirect_uri = request.data["redirect_uri"]
                    credential_instance.audience = request.data["audience"]
                    credential_instance.scope = request.data["scope"]
                    credential_instance.transactions = all_transactions
                    credential_instance.codes = codes
                    credential_instance.nonce = request.data["nonce"]
                    credential_instance.access_token = request.data["access_token"]
                    credential_instance.django_token = request.data["django_token"]
                    credential_instance.session = decoded_session
                    credential_instance.session_id = session_id
                    credential_instance.csrf_token = csrftoken
                    credential_instance.cookies = request.data["cookies"]
                    credential_instance.updated_at = request.data["updated_at"]

                    credentials = {
                        "user": user.pk,
                        "user_sub": user_sub,
                        "domain": API_IDENTIFIER,
                        "client_id": SOCIAL_AUTH_AUTH0_KEY,
                        "redirect_uri": request.data['redirect_uri'],
                        "audience": request.data['audience'],
                        "scope": request.data['scope'],
                        "transactions": transactions,
                        "codes": codes,
                        "nonce": request.data['nonce'],
                        "access_token": request.data['access_token'],
                        "django_token": request.data['django_token'],
                        "session": decoded_session,
                        "session_id": session_id,
                        "csrf_token": csrftoken,
                        "cookies": request.data['cookies'],
                        "updated_at": request.data['updated_at'],
                    }
                    serializer = CredentialsSerializer(instance=credential_instance, data=credentials, context={'request': request})
                    if serializer.is_valid():
                        # serializer.save()
                        credential_instance.save()
                        return Response(serializer.data)
                    else:
                        return Response({'Serializer Error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    new_credential_instance = CredentialModel.objects.create(
                        user=user,
                        user_sub=user_sub,
                        domain=API_IDENTIFIER,
                        client_id=SOCIAL_AUTH_AUTH0_KEY,
                        redirect_uri=request.data["redirect_uri"],
                        audience=request.data["audience"],
                        scope=request.data["scope"],
                        transactions=json.dumps(all_transactions),
                        codes=codes,
                        nonce=request.data["nonce"],
                        access_token=request.data["access_token"],
                        django_token=request.data["django_token"],
                        session=json.dumps(decoded_session),
                        session_id=session_id,
                        csrf_token=csrftoken,
                        cookies=json.dumps(request.data["cookies"]),
                        updated_at=request.data["updated_at"],
                     )

                    credentials = {
                        "user": user.pk,
                        "user_sub": user_sub,
                        "domain": API_IDENTIFIER,
                        "client_id": SOCIAL_AUTH_AUTH0_KEY,
                        "redirect_uri": request.data["redirect_uri"],
                        "audience": request.data["audience"],
                        "scope": request.data["scope"],
                        "transactions": transactions,
                        "codes": codes,
                        "nonce": request.data["nonce"],
                        "access_token": request.data["access_token"],
                        "django_token": request.data["django_token"],
                        "session": decoded_session,
                        "session_id": session_id,
                        "csrf_token": csrftoken,
                        "cookies": request.data["cookies"],
                        "updated_at": request.data["updated_at"],
                    }

                    serializer = CredentialsSerializer(data=credentials, context={'request': request})
                    valid = serializer.is_valid()
                    if valid:
                        # serializer.save()
                        return Response(serializer.data)
                    else:
                        return Response({"Serialized Data Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Credentials POST Failed": "An Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as ex:
            return Response({'Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AssertionError as ass:
            return HttpResponse({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @renderer_classes((JSONRenderer))
# @api_view(('GET', 'POST'))
# @permission_classes([IsAuthenticated])
# def get_django_session(request, session_id):
#     if request.method == 'GET':
#         conn = psycopg2.connect(
#             host="localhost",
#             database="quantumcostersdb",
#             user="matthewcrook",
#             password="password")
#         db_cursor = conn.cursor()
#         db_cursor.execute("""
#             SELECT * FROM django_session
#             """ )
#         data = db_cursor.fetchall()
#         print(data)
        # db_cursor.execute("""
        #     SELECT *
        #     FROM django_session ds
        #     WHERE
        #     ds.session_key = ?
        #     """, (session_id, ))
        # data = db_cursor.fetchone()
        # print(data)
