from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import login
from django.contrib.auth import authenticate

from quantumapi.models import UserProfile, Credential
from rest_auth.models import TokenModel
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes

from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmation
from social_django.models import UserSocialAuth, Association, Nonce, DjangoAssociationMixin, DjangoUserMixin, Code, DjangoCodeMixin

from .management_api_services import management_api_oath_endpoint, get_management_api_user, get_open_id_config, get_management_api_grants, jwks_endpoint

from django.contrib.auth.views import auth_login
from rest_framework.authentication import authenticate

from social_django.views import auth, do_auth
from social_django.context_processors import backends, user_backends_data
from social_django.storage import DjangoUserMixin

from django.contrib.auth.backends import AllowAllUsersRemoteUserBackend, AllowAllUsersModelBackend, RemoteUserBackend
from social_core.strategy import OpenIdStore, DEFAULT_AUTH_PIPELINE, BaseStrategy
from social_core.backends.auth0 import Auth0OAuth2

from social_core.actions import user_is_authenticated, user_is_active

# from social_core.pipeline.social_auth import associate_user
from django.middleware.csrf import get_token
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_OPEN_ID_SERVER_URL, SOCIAL_AUTH_STRATEGY, SOCIAL_AUTH_AUTH0_KEY, SOCIAL_AUTH_AUTH0_SECRET
from jose import jwt
import json
import datetime

from allauth.socialaccount.views import  get_current_site
from allauth.socialaccount.models import SocialToken, SocialApp, SocialLogin, SocialAccount




@api_view(('GET', 'POST'))
def login_user(request):
    try:
        req_body = json.loads(request.body.decode())

        if request.method == 'POST':
            user = request.user
            is_authenticated = user_is_authenticated(user)

            if user.email == req_body['email'] and user.auth0_identifier.split('.')[1] == req_body['password'] and is_authenticated:
                email = req_body['email']
                password = user.auth0_identifier.split('.')[1]
                auth0_identifier = req_body['uid']
                auth0_uid = auth0_identifier.replace("|", ".")
                authenticated_user = authenticate(auth0_identifier=auth0_uid, password=password)

                if authenticated_user is not None:
                    remote_user_auth = request.successful_authenticator.authenticate(request)

                    if remote_user_auth is not None:
                        management_api_oauth_endpoint_result = management_api_oath_endpoint(AUTH0_DOMAIN)
                        management_api_token = json.loads(management_api_oauth_endpoint_result)
                        management_api_jwt = management_api_token['access_token']
                        management_api_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])

                        user_django_token = TokenModel.objects.get(user=authenticated_user)
                        social_user = authenticated_user.social_auth.get(provider='auth0')
                        remote_authenticated_user = remote_user_auth[0]

                        # backend_data = backends(request)
                        # user_current_backend = authenticated_user.backend
                        # storage = authenticated_user.storage
                        # user_backend_data = user_backends_data(remote_authenticated_user, backend_data, storage)
                        # print("user_backend_data: login.py:", user_backends_data)

                        if user_django_token is not None:
                            token = user_django_token
                        else:
                            token = TokenModel.objects.create(user=authenticated_user)

                        key = token.key
                        provider = social_user.provider
                        extra_data = req_body['extra_data']
                        extra_data['access_token'] = request.auth
                        id_token = json.loads(req_body['id_token'])
                        nonce = id_token['nonce']
                        exp = id_token['exp']
                        iat = id_token['iat']
                        assoc_type = "username-password-authentication"

                        if 'csrf_token' in req_body and req_body['csrf_token']:
                            csrf = req_body['csrf_token']
                        else:
                            csrf = get_token(request)

                        # is_active = user_is_active(authenticated_user)

                        account_email = EmailAddress.objects.get(user_id=remote_authenticated_user.id)
                        user_social_auth = UserSocialAuth.objects.get(user_id=remote_authenticated_user.id)

                        # Get the most recent entry on Credentials, which would have just posted/ updated
                        # from the user logging in thru auth0. (In App.js and Auth0Context)
                        credentials = Credential.objects.get(user_id=authenticated_user.id)
                        all_transactions = json.loads(credentials.transactions)
                        transaction_items_keys = all_transactions['transactions'].keys()
                        transactions_values = all_transactions['transactions'].values()

                        codes = []
                        print("transaction_items_keys", transaction_items_keys)
                        for c in transaction_items_keys:
                            codes.append(c)

                        transactions = []
                        print('transactions_values', transactions_values)
                        for t in transactions_values:
                            transactions.append(t)

                        user_association = Association.objects.get(server_url=AUTH0_OPEN_ID_SERVER_URL)
                        code_verifier = transactions[0]['code_verifier'] if len(transactions) > 0 else {}
                        social_account = SocialAccount.objects.get(user_id=remote_authenticated_user.id)

                        social_token = SocialToken.objects.get(account_id=social_account.id)
                        social_token.token = id_token
                        social_token.token_secret = request.auth
                        time_now = datetime.datetime.now()
                        expires_at = time_now + datetime.timedelta(0, exp)
                        social_token.expires_at = expires_at
                        social_token.save()

                        social_app = SocialApp.objects.get(provider=provider)

                        login(request, social_user.user, backend='quantumapi.auth0_backend.Auth0')
                        session_user = request.session
                        is_session = Session.objects.filter(session_key=session_user.session_key).exists()

                        try:
                            if is_session:
                                session = Session.objects.get(session_key=session_user.session_key)
                                decoded_session = session.get_decoded()
                                session.save()
                            else:
                                session = Session.objects.create(user=remote_authenticated_user)
                                session.save()


                            auth_user = {
                                    "valid": True,
                                    "id": user.id,
                                    "first_name": user.first_name,
                                    "last_name": user.last_name,
                                    "email": user.email,
                                    "username": user.username,
                                    "auth0_identifier": user.auth0_identifier,
                                    "QuantumToken": key,
                                    "accessToken": remote_user_auth[1],
                                    "management_api_token": management_api_token,
                                    "session": session.session_key,
                                    'csrf': csrf,
                                    # 'user_association': user_association.id,
                                    'user_social_auth': user_social_auth.id,
                                    'account_email': account_email.id,
                                    'management_user': management_api_user,
                                    'social_account': social_account.id,
                                    'social_app': social_app.id,
                                    'email_confirmation': True,
                                }

                            data = json.dumps(auth_user)
                            return HttpResponse(data, content_type='application/json')
                        except Exception as ex:
                            return Response({'Final data Validation Error': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        data = json.dumps({"valid": False, "Error": 'Remote User un authenticated or None.'})
                        return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
                    return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                data = json.dumps({"valid": False, "Error": 'Email did not match email we have for this accout.'})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as ex:
        return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
