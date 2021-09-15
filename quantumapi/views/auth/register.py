from django.http import HttpResponse, HttpResponseServerError
from rest_framework.response import Response

from django.contrib.auth import login, authenticate
from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication, RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import DjangoModelPermissions

from quantumapi.models import UserProfile
from quantumapi.models import User as UserModel
from rest_auth.models import TokenModel
from django.contrib.sessions.models import Session
from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmation
from social_django.models import UserSocialAuth, Association, Nonce, Code, Association
from django.contrib.auth import get_user_model
from ..user import UserSerializer

from allauth.socialaccount.models import SocialToken, SocialApp, SocialLogin, SocialAccount


from .login import login_user
from django.middleware.csrf import get_token
from social_core.pipeline.social_auth import associate_user
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_OPEN_ID_SERVER_URL, SOCIAL_AUTH_AUTH0_SECRET, SOCIAL_AUTH_AUTH0_KEY
from social_django.context_processors import backends, user_backends_data
from .management_api_services import management_api_oath_endpoint, get_management_api_user

from django.contrib.auth.views import auth_login
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import set_cookie_with_token


from allauth.socialaccount.views import  get_current_site


# from jose import jwt
import datetime
import json
#import http.client


@api_view(('GET', 'POST'))
@authentication_classes([SessionAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def register_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body.decode())

            UserModel = get_user_model()
            user = UserModel.objects.get(auth0_identifier=req_body['auth0_identifier'])

            user.first_name = req_body['first_name']
            user.last_name = req_body['last_name']
            user.username = req_body['username']
            user.email = req_body['email']
            password = request.user.auth0_identifier.split('.')[1]
            user.set_password(password)
            user.save()

            new_userprofile = UserProfile.objects.create(
                address=req_body["address"],
                user=user
            )
            new_userprofile.save()

            # email = req_body['email']
            authenticated_user = authenticate(auth0_identifier=req_body['auth0_identifier'], password=password)

            if authenticated_user is not None:
                remote_authenticated_user = request.successful_authenticator.authenticate(request)

                if remote_authenticated_user is not None:
                    management_api_token_endpoint = management_api_oath_endpoint(AUTH0_DOMAIN)
                    management_api_token = json.loads(management_api_token_endpoint)
                    management_api_jwt = management_api_token['access_token']
                    management_api_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])

                    token = TokenModel.objects.create(user=remote_authenticated_user[0])
                    key = token.key

                    extra_data = req_body['extra_data']
                    extra_data['access_token'] = remote_authenticated_user[1]

                    # backend_data = backends(request)
                    #user_current_backend = authenticated_user.backend

                    #auth0_backend = backend_data['backends']['backends'][1]
                    #openId_backend = backend_data['backends']['backends'][0]
                    #associated_backends = backend_data['backends'].get('associated')

                    # return csrf token for POST form. side effect is have @csrf_protect
                    csrf = req_body['csrf_token'] if 'csrf_token' in req_body and req_body['csrf_token'] else get_token(request)
                    id_token = json.loads(req_body['id_token'])
                    nonce = id_token['nonce']
                    exp = id_token['exp']
                    iat = id_token['iat']
                    extra_data = req_body['extra_data']
                    extra_data['access_token'] = id_token['__raw']
                    identities = management_api_user.get('identities')[0]
                    provider = identities.get('provider')

                    # The 'connection' in the auth0 returned result
                    assoc_type = identities.get('connection')

                    all_transactions = req_body['transactions']
                    transaction_items_keys = all_transactions.keys()
                    transactions_values = all_transactions.values()

                    codes = [c for c in transaction_items_keys]
                    transactions = [t for t in transactions_values]

                    # handles = [handle for handle in codes] if len(codes) > 0 else {}
                    # code_verifiers = [code['code_verifier'] for code in transactions] if len(transactions) > 0 else {}
                    handle = transactions[0]['nonce'] if len(transactions) > 0 else {}
                    code_verifier = transactions[0]['code_verifier'] if len(transactions) > 0 else {}

                    # code = codes[0] if len(codes) > 0 else {}


                    # associate_user('openid', social_user.uid, authenticated_user, social_user)
                    social_user = remote_authenticated_user[0].social_auth.get_or_create(user_id=remote_authenticated_user[0].id, provider=provider, extra_data=extra_data, uid=req_body['auth0_identifier'].replace(".", "|"))
                    # is_association = Association.objects.filter(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=handle).exists()

                    if Association.objects.filter(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=handle).exists():
                        user_association = Association.objects.get(server_url=AUTH0_OPEN_ID_SERVER_URL, handle=handle)
                    else:
                        user_association = Association.objects.create(
                            server_url=AUTH0_OPEN_ID_SERVER_URL,
                            handle=handle,
                            secret=code_verifier,
                            issued=iat,
                            lifetime=exp,
                            assoc_type=assoc_type
                            )

                    social_account = SocialAccount()
                    social_account.user = remote_authenticated_user[0]
                    social_account.uid = req_body['uid']
                    social_account.provider = provider
                    social_account.extra_data = management_api_user
                    social_account.save()

                    account_email = EmailAddress.objects.get_or_create(
                        user=social_account.user,
                        email=authenticated_user.email,
                        verified=True,
                        primary=True
                        )

                    social_auth_nonce = Nonce.objects.create(server_url=AUTH0_OPEN_ID_SERVER_URL, timestamp=iat, salt=nonce)
                    user_socialauth_code = Code.objects.create(email=account_email[0], code=codes[0], verified=True)

                    social_app = SocialApp.objects.get_or_create(
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
                        app_id=social_app[0].id,
                        account_id=social_account.id,
                        token=id_token,
                        token_secret=id_token['__raw'],
                        expires_at=expires_at
                        )

                    # Changed from user to authenticated_user
                    login(request, social_user[0].user, backend='quantumapi.auth0_backend.Auth0')

                    current_user_session = request.session
                    is_session = Session.objects.filter(session_key=current_user_session.session_key).exists()

                    if is_session:
                        session = Session.objects.get(session_key=current_user_session.session_key)
                    else:
                        session = Session.objects.create(user=authenticated_user)
                        # session.save()

                    email_confirmation = EmailConfirmation.objects.get_or_create(
                        email_address=account_email[0],
                        key=session.session_key,
                        sent=datetime.datetime.now()
                        )

                    # Turning into Set then back to List to filter out Duplicates (#ToDo-not needed.)
                    social_app_to_list = list(social_app)
                    social_app_data = social_app_to_list[0]

                    auth_user = {
                        "valid": True,
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "username": user.username,
                        "is_staff": user.is_staff,
                        "auth0_identifier": user.auth0_identifier,
                        "QuantumToken": key,
                        "session": session.session_key,
                        'csrf': csrf,
                        'user_social_auth_id': social_user[0].id,
                        'account_email_id': account_email[0].id,
                        'management_user': management_api_user,
                        'social_account_id': social_account.id,
                        'social_app_id': social_app_data.id,
                        'social_app_name': social_app_data.name,
                        "social_token_id": social_token.id,
                        'association_id': user_association.id,
                        'email_confirmation': True,
                        'user_profile_id': new_userprofile.id,
                    }

                    data = json.dumps({"DjangoUser": auth_user})
                    return HttpResponse(data, content_type='application/json')
                else:
                    error = "Remote authentication failed. Remote Authenticated User was None."
                    data = json.dumps({"Remote Authentication Error": error})
                    return HttpResponse(data, content_type='application/json')
            else:
                error = "Authentication failed. Authenticated User was None."
                data = json.dumps({"Authentication Error": error})
                return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response(ex.args, content_type='application/json')
