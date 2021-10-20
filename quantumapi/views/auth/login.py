from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate

from quantumapi.models import Credential
from rest_auth.models import TokenModel
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.renderers import JSONRenderer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


from allauth.account.models import EmailAddress
# from allauth.account.models import EmailConfirmation
from social_django.models import UserSocialAuth, Association, Nonce, DjangoAssociationMixin, DjangoUserMixin, Code, DjangoCodeMixin

from .management_api_services import management_api_oath_endpoint, get_management_api_user, retrieve_user_logs

# from django.contrib.auth.views import auth_login
from rest_framework.authentication import authenticate

# from social_django.views import auth, do_auth
# from social_django.context_processors import backends, user_backends_data
# from social_django.storage import DjangoUserMixin

# from django.contrib.auth.backends import AllowAllUsersRemoteUserBackend, AllowAllUsersModelBackend, RemoteUserBackend
# from social_core.strategy import OpenIdStore, DEFAULT_AUTH_PIPELINE, BaseStrategy
# from social_core.backends.auth0 import Auth0OAuth2

from social_core.actions import user_is_authenticated, user_is_active

# from social_core.pipeline.social_auth import associate_user
from django.middleware.csrf import get_token
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_OPEN_ID_SERVER_URL, SOCIAL_AUTH_AUTH0_KEY, SOCIAL_AUTH_AUTH0_SECRET
# from jose import jwt
import json
import datetime

# from allauth.socialaccount.views import  get_current_site
from allauth.socialaccount.models import SocialToken, SocialApp, SocialLogin, SocialAccount

from rest_framework_jwt.authentication import JSONWebTokenAuthentication





@api_view(('GET', 'POST'))
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def login_user(request):
    try:
        req_body = json.loads(request.body.decode())

        if request.method == 'POST':
            user = request.user
            is_authenticated = user_is_authenticated(user)
            id_token = json.loads(req_body['id_token'])

            if user.email == req_body['email'] and user.auth0_identifier.split('.')[1] == id_token['sub'].split('|')[1] and is_authenticated:
                # email = req_body['email']
                # password = user.auth0_identifier.split('.')[1]
                password = id_token['sub'].split('|')[1]
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

                        if user_django_token is not None:
                            token = user_django_token
                        else:
                            token = TokenModel.objects.create(user=authenticated_user)

                        key = token.key
                        extra_data = req_body['extra_data']
                        extra_data['access_token'] = remote_authenticated_user[1]
                        extra_data['id_token__raw'] = id_token['__raw']
                        nonce = id_token['nonce']
                        exp = id_token['exp']
                        iat = id_token['iat']
                        connection = management_api_user.get('identities')[0]
                        assoc_type = connection.get('connection')
                        provider = social_user.provider

                        if 'csrf_token' in req_body and req_body['csrf_token']:
                            csrf = req_body['csrf_token']
                        else:
                            csrf = get_token(request)

                        # is_active = user_is_active(authenticated_user)
                        account_email = EmailAddress.objects.get(user_id=remote_authenticated_user.id)
                        user_social_auth = UserSocialAuth.objects.get(user_id=remote_authenticated_user.id)
                        social_account = SocialAccount.objects.get(user_id=remote_authenticated_user.id)
                        social_app = SocialApp.objects.get_or_create(
                            provider=provider,
                            name="Quantum Coasters",
                            secret=SOCIAL_AUTH_AUTH0_SECRET,
                            client_id=AUTH0_CLIENT_ID,
                            key=SOCIAL_AUTH_AUTH0_KEY
                            )

                        time_now = datetime.datetime.now()
                        # social_token = SocialToken.objects.get_or_create(
                        #     account=social_account,
                        #     token=user_social_auth.access_token,
                        #     token_secret=user_social_auth.tokens,
                        #     expires_at = time_now + datetime.timedelta(0, exp),
                        #     app = social_app[0]
                        #     )
                        social_token = SocialToken.objects.get(account_id=social_account.id) if SocialToken.objects.filter(account_id=social_account.id).exists() else SocialToken(account=social_account)
                        social_token.token = user_social_auth.access_token
                        social_token.token_secret = user_social_auth.tokens
                        time_now = datetime.datetime.now()
                        expires_at = time_now + datetime.timedelta(0, exp)
                        social_token.expires_at = expires_at
                        social_token.app = social_app[0]
                        social_token.save()


                        # login user, then grab the credentials and newly created session which is going to be called and returned after login.
                        login(request, social_user.user, backend='quantumapi.auth0_backend.Auth0')

                        try:
                            session_user = request.session
                            is_session = Session.objects.filter(session_key=session_user.session_key).exists()
                            if is_session:
                                session = Session.objects.get(session_key=session_user.session_key)
                                # decoded_session = session.get_decoded()
                                # session.save()
                            else:
                                session = Session.objects.create(user=remote_authenticated_user)
                                # session.save()

                            # Get the most recent entry on Credentials, which would have just posted/ updated
                            # from the user logging in thru auth0. (In App.js and Auth0Context)
                            has_credentials = Credential.objects.filter(user_id=authenticated_user.id).exists()
                            credentials = Credential.objects.filter(user_id=authenticated_user.id).latest() if has_credentials else None
                            # To break login...
                            # credentials = Credential.objects.get(user_id=authenticated_user.id)

                            if credentials is not None:
                                # all_transactions = json.loads(credentials.transactions)
                                # transaction_items_keys = all_transactions['transactions'].keys()
                                # transactions_values = all_transactions['transactions'].values()

                                # codes = [c for c in transaction_items_keys]
                                # transactions = [t for t in transactions_values]

                                #handles = [handle for handle in codes] if len(codes) > 0 else {}
                                #code_verifiers = [code['code_verifier'] for code in transactions] if len(transactions) > 0 else {}
                                # handle = transactions[0]['nonce'] if len(transactions) > 0 else {}
                                # code_verifier = transactions[0]['code_verifier'] if len(transactions) > 0 else {}
                                code_verifier = retrieve_user_logs(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])
                                seacft = [l for l in code_verifier if l['type'] == 'seacft']
                                seacft_details = seacft[0].get('details')
                                code = seacft_details.get('code')

                                #all_backends = backends(request)
                                #user_backends = all_backends.get('backends')
                                #auth0_backend = user_backends['backends'][1]
                                #openId_backend = user_backends['backends'][0]
                                #user_assoc_backends = user_backends.get('associated')

                                if Association.objects.filter(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=nonce).exists():
                                    Association.objects.get(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=nonce)
                                else:
                                    Association.objects.create(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=nonce, secret=code, issued=iat, lifetime=exp, assoc_type=assoc_type)

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
                                        "csrf": csrf,
                                        "user_social_auth": user_social_auth.id,
                                        "account_email": account_email.id,
                                        "management_user": management_api_user,
                                        "social_account": social_account.id,
                                        "social_app": social_app[0].id,
                                        "email_confirmation": True,
                                        "has_credentials": True,
                                        "credentials_id": credentials.id
                                    }
                                data = json.dumps(auth_user)
                                return HttpResponse(data, content_type='application/json')

                            else:
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
                                    "csrf": csrf,
                                    "user_social_auth": user_social_auth.id,
                                    "account_email": account_email.id,
                                    "management_user": management_api_user,
                                    "social_account": social_account.id,
                                    "social_app": social_app[0].id,
                                    "email_confirmation": True,
                                    "has_credentials": False,
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
                data = json.dumps({"valid": False, "Message": 'Email did not match email we have for this accout.'})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as ex:
        return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
