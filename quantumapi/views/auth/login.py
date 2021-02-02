from django.http import HttpResponse
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

            if user.email == req_body['email']:
                email = req_body['email']
                password = req_body['password']
                auth0_identifier = req_body['uid']
                auth0_uid = auth0_identifier.replace("|", ".")
                authenticated_user = authenticate(auth0_identifier=auth0_uid, password=password)

                if authenticated_user is not None:
                    remote_user_auth = request.successful_authenticator.authenticate(request)
                    token = TokenModel.objects.get(user=authenticated_user)

                    social_user = authenticated_user.social_auth.get(provider='auth0')
                    backend_data = backends(request)
                    print('Login quantumapi:request_backends', backend_data)
                    user_current_backend = authenticated_user.backend
                    storage = authenticated_user.storage
                    user_backend_data = user_backends_data(authenticated_user, backend_data, storage)

                    association = storage.association
                    code = storage.code
                    nonce = storage.nonce
                    partial = storage.partial
                    user_from_storage = storage.user

                    if token is not None:
                        token = TokenModel.objects.get(user=authenticated_user)
                    else:
                        token = TokenModel.objects.create(user=authenticated_user)

                    key = token.key
                    provider = req_body['provider']
                    extra_data = req_body['extra_data']
                    id_token = json.loads(req_body['id_token'])
                    nonce = id_token['nonce']
                    exp = id_token['exp']
                    iat = id_token['iat']
                    assoc_type = "username-password-authentication"

                    if 'csrf_token' in req_body and req_body['csrf_token']:
                        csrf = req_body['csrf_token']
                    else:
                        csrf = get_token(request)

                    # auth_login(request, authenticated_user, backend='django.contrib.auth.backends.RemoteUserBackend')
                    login(request, social_user)

                    auth_user_backends = backends(request)
                    is_active = user_is_active(authenticated_user)
                    is_authenticated = user_is_authenticated(authenticated_user)
                    # associated_socialauth_backend_users = request_backends['backends']['associated']
                    # socialauth_user = associated_socialauth_backend_users.get(user=authenticated_user)

                    # from_db = socialauth_user.from_db()
                    # get_access_token = socialauth_user.get_access_token(SOCIAL_AUTH_STRATEGY)
                    # get_social_auth_for_user = socialauth_user.get_social_auth_for_user(authenticated_user)

                    # auth_user_usersocialauth = associate_user(backend='django.contrib.auth.backends.RemoteUserBackend', uid=req_body['uid'], user=authenticated_user)

                    session_user = request.session
                    is_session = Session.objects.filter(session_key=session_user.session_key).exists()
                    is_account_email = EmailAddress.objects.filter(user_id=authenticated_user.id).exists()
                    is_user_social_auth = UserSocialAuth.objects.filter(user_id=authenticated_user.id).exists()
                    # Get the most recent entry on Credentials, which would have just posted/ updated from the user logging in thru auth0. (In App.js and Auth0Context)

                    management_api_token = management_api_oath_endpoint(AUTH0_DOMAIN)
                    management_api_token = json.loads(management_api_token)
                    management_api_jwt = management_api_token['access_token']
                    management_api_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])

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

                    try:
                        if is_session:
                            session = Session.objects.get(session_key=session_user.session_key)
                            decoded_session = session.get_decoded()
                            session.save()
                        else:
                            session = request.session
                            session.save()

                        if is_account_email:
                                account_email = EmailAddress.objects.get(user_id=authenticated_user.id)
                        else:
                            account_email = EmailAddress.objects.create(
                                user=authenticated_user,
                                email=user.email,
                                verified=True,
                                primary=True
                                )
                            email_confirmation = EmailConfirmation.objects.create(
                                email_address=account_email,
                                key=session.session_key,
                                sent=datetime.datetime.now()
                                )

                        # Get social auth login for user
                        if is_user_social_auth:
                            associated_socialauth_backend_users = request_backends['backends']['associated']
                            user_social_auth = associated_socialauth_backend_users.get(user=authenticated_user)
                            # user_social_auth = UserSocialAuth.objects.get(uid=req_body['uid'])
                            user_association = Association.objects.get(server_url=AUTH0_OPEN_ID_SERVER_URL)
                            code_verifier = transactions[0]['code_verifier'] if len(transactions) > 0 else {}
                            # social_auth_nonce = Nonce.objects.create(server_url=codes[0], timestamp=iat, salt=nonce)
                            # user_socialauth_code = Code.objects.create(email=account_email, code=codes[0], verified=True)
                            social_account = SocialAccount.objects.get(user_id=authenticated_user.id)
                            social_token = SocialToken.objects.get(account_id=social_account.id)
                            social_token.token = remote_user_auth[1]
                            social_token.token_secret = management_api_jwt
                            time_now = datetime.datetime.now()
                            expires_at = time_now + datetime.timedelta(0, exp)
                            social_token.expires_at = expires_at
                            social_token.save()
                            social_app = SocialApp.objects.get(provider=provider)
                        else:

                            social_auth = create_user_association(request, token, transactions, codes, account_email, auth0_identifier, management_api_user, remote_user_auth, management_api_jwt, authenticated_user)

                            user_social_auth = social_auth['user_social_auth']
                            user_association = social_auth['user_association']
                            social_auth_nonce = social_auth['social_auth_nonce']
                            user_socialauth_code = social_auth['user_socialauth_code']
                            social_account = social_auth['social_account']
                            social_app = social_auth['social_app']
                            social_token = social_auth['social_token']


                        auth_user = {
                                "valid": True,
                                "id": user.id,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email,
                                "username": user.username,
                                "auth0_identifier": user.auth0_identifier,
                                "QuantumToken": key,
                                "session": session.session_key,
                                'csrf': csrf,
                                # 'user_association': user_association.id,
                                'user_social_auth': user_social_auth.id,
                                'account_email': account_email.id,
                                'management_user': json.dumps(management_api_user),
                                'social_account': social_account.id,
                                'social_app': social_app.id,
                                'email_confirmation': True,
                            }

                        data = json.dumps(auth_user)
                        return HttpResponse(data, content_type='application/json')
                    except Exception as ex:
                        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def create_user_association(request, token, transactions, codes, account_email, auth0_identifier, management_api_user, remote_user_auth, management_api_jwt, authenticated_user):

    req_body = json.loads(request.body.decode())

    key = token.key
    provider = req_body['provider']
    extra_data = req_body['extra_data']
    id_token = json.loads(req_body['id_token'])
    nonce = id_token['nonce']
    exp = id_token['exp']
    iat = id_token['iat']
    assoc_type = "username-password-authentication"


    user_social_auth = UserSocialAuth.objects.create(
            user=authenticated_user,
            uid=req_body['uid'],
            provider=provider,
            extra_data=extra_data)

    code_verifier = transactions[0]['code_verifier'] if len(transactions) > 0 else {}
    code = codes[0] if len(codes) > 0 else {}
    is_association = Association.objects.filter(server_url=AUTH0_OPEN_ID_SERVER_URL).exists()

    if is_association:
        user_association = Association.objects.get(server_url=AUTH0_OPEN_ID_SERVER_URL)
    else:
        user_association = Association.objects.create(
            server_url=AUTH0_OPEN_ID_SERVER_URL,
            handle=nonce,
            secret=code_verifier,
            issued=iat,
            lifetime=exp,
            assoc_type=assoc_type
            )

    social_auth_nonce = Nonce.objects.create(server_url=AUTH0_OPEN_ID_SERVER_URL, timestamp=iat, salt=nonce)
    user_socialauth_code = Code.objects.create(email=account_email, code=code, verified=True)

    social_account = SocialAccount()
    social_account.user = authenticated_user
    social_account.uid = auth0_identifier
    social_account.provider = provider
    social_account.extra_data = management_api_user
    social_account.save()

    social_app = SocialApp.objects.create(
        provider=provider,
        name="Quantum Coasters",
        secret=SOCIAL_AUTH_AUTH0_SECRET,
        client_id=AUTH0_CLIENT_ID,
        key=SOCIAL_AUTH_AUTH0_KEY
        )

    time_now = datetime.datetime.now()
    expires_at = time_now + datetime.timedelta(0, exp)
    # time = expires_at.time()

    social_token = SocialToken.objects.create(
        app_id=social_app.id,
        account_id=social_account.id,
        token=remote_user_auth[1],
        token_secret=management_api_jwt,
        expires_at=expires_at
        )

    login_data = {
        'user_social_auth': user_social_auth,
        'user_association': user_association,
        'social_auth_nonce': social_auth_nonce,
        'user_socialauth_code': user_socialauth_code,
        'social_account': social_account,
        'social_app': social_app,
        'social_token': social_token,
    }

    return login_data













                            # user_social_auth = UserSocialAuth.objects.create(
                            #     user=authenticated_user,
                            #     uid=req_body['uid'],
                            #     provider=provider,
                            #     extra_data=extra_data)

                            # code_verifier = transactions[0]['code_verifier']
                            # user_association = Association.objects.create(
                            #     server_url=codes[0],
                            #     handle=nonce,
                            #     secret=code_verifier,
                            #     issued=iat,
                            #     lifetime=exp,
                            #     assoc_type=assoc_type
                            #     )
                            # social_auth_nonce = Nonce.objects.create(server_url=codes[0], timestamp=iat, salt=nonce)
                            # user_socialauth_code = Code.objects.create(email=account_email, code=codes[0], verified=True)

                        # management_api_token = management_api_oath_endpoint(AUTH0_DOMAIN)
                        # management_api_token = json.loads(management_api_token)
                        # management_api_jwt = management_api_token['access_token']
                        # management_api_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])
                        # management_api_open_id_config = get_open_id_config(AUTH0_DOMAIN, management_api_jwt)
                        # management_api_grants = get_management_api_grants(AUTH0_DOMAIN, management_api_jwt)
                        # jwks = jwks_endpoint(AUTH0_DOMAIN, management_api_jwt)

                            # social_account = SocialAccount()
                            # social_account.user = authenticated_user
                            # social_account.uid = auth0_identifier
                            # social_account.provider = provider
                            # social_account.extra_data = management_api_user
                            # social_account.save()

                        # get associated backends in request to put as email.
                        # social_login = SocialLogin()
                        # social_login.user = remote_user_auth[0]
                        # social_login.account = social_account
                        # social_login.state = social_login.state_from_request(request)
                        # social_login.token = remote_user_auth[1]
                        # associate emails to queryset of emails pertaining to backend...if user already
                        # social_login.email_addresses = account_email
                        # social_login.save(request, connect=False)
                        # social_login.connect(request, social_account)

                        # social_state = social_user.state_from_request(request)
                        # social_stash_state = social_user.stash_state(request)

                        # social_user_serialize = social_user.serialize()
                        # social_user_login_connect = social_login.connect(request, social_account)

                            # social_app = SocialApp.objects.create(
                            #     provider=provider,
                            #     name="Quantum Coasters",
                            #     secret=SOCIAL_AUTH_AUTH0_SECRET,
                            #     client_id=AUTH0_CLIENT_ID,
                            #     key=SOCIAL_AUTH_AUTH0_KEY
                            #     )

                            # time_now = datetime.datetime.now()
                            # expires_at = time_now + datetime.timedelta(0, exp)
                            # # time = expires_at.time()

                            # social_token = SocialToken.objects.create(
                            #     app_id=social_app.id,
                            #     account_id=social_account.id,
                            #     token=remote_user_auth[1],
                            #     token_secret=management_api_jwt,
                            #     expires_at=expires_at
                            #     )
