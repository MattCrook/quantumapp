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
# from social_core.pipeline.social_auth import associate_user
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_OPEN_ID_SERVER_URL, SOCIAL_AUTH_AUTH0_SECRET, SOCIAL_AUTH_AUTH0_KEY
from social_django.context_processors import backends
from .management_api_services import management_api_oath_endpoint, get_management_api_user

from django.contrib.auth.views import auth_login
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import set_cookie_with_token


from allauth.socialaccount.views import  get_current_site


from jose import jwt
import datetime
import json
import http.client


@api_view(('GET', 'POST'))
@authentication_classes([SessionAuthentication, JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def register_user(request):
    try:
        if request.method == 'POST':
            req_body = json.loads(request.body.decode())
            request_backends = backends(request)
            print(request_backends)


            UserModel = get_user_model()
            user = UserModel.objects.get(auth0_identifier=req_body['auth0_identifier'])

            user.first_name = req_body['first_name']
            user.last_name = req_body['last_name']
            user.username = req_body['username']
            user.email = req_body['email']
            password = req_body['password']
            user.set_password(password)
            user.save()

            new_userprofile = UserProfile.objects.create(
                address=req_body["address"],
                user=user
            )
            new_userprofile.save()

            email = req_body['email']
            authenticated_user = authenticate(auth0_identifier=req_body['auth0_identifier'], password=password)

            if authenticated_user is not None:
                backend = authenticated_user.backend
                remote_authenticated_user = request.successful_authenticator.authenticate(request)
                # associate_user('django.contrib.auth.backends.RemoteUserBackend', req_body['uid'], user, req_body['provider'])
                # UserModel.blacklistedtoken_set.related_manager_cls.create()
                # UserModel.socialaccount_set.related_manager_cls.create()

                token = TokenModel.objects.create(user=authenticated_user)

                key = token.key
                # return csrf token for POST form. side effect is have @csrf_protect
                csrf = get_token(request)
                provider = req_body['provider']
                extra_data = req_body['extra_data']
                id_token = json.loads(req_body['id_token'])
                nonce = id_token['nonce']
                exp = id_token['exp']
                iat = id_token['iat']
                assoc_type = "username-password-authentication"

                auth_login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')

                current_user_session = request.session
                is_session = Session.objects.filter(session_key=current_user_session.session_key).exists()
                # is_account_email = EmailAddress.objects.filter(user_id=user.id).exists()
                # is_user_social_auth = UserSocialAuth.objects.filter(user_id=user.id).exists()

                if is_session:
                    session = Session.objects.get(session_key=current_user_session.session_key)
                    session.save()
                else:
                    session = Session.objects.create(user=authenticated_user)
                    session.save()

                management_api_token = management_api_oath_endpoint(AUTH0_DOMAIN)
                management_api_token = json.loads(management_api_token)
                management_api_jwt = management_api_token['access_token']
                management_api_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])


                all_transactions = req_body['transactions']
                transaction_items_keys = all_transactions['transactions'].keys()
                transactions_values = all_transactions['transactions'].values()

                transactions = []
                for t in transactions_values:
                    transactions.append(t)

                codes = []
                for c in transaction_items_keys:
                    codes.append(c)


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

                user_social_auth = UserSocialAuth.objects.create(
                    user=authenticated_user,
                    uid=req_body['uid'],
                    provider=provider,
                    extra_data=extra_data
                    )


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
                social_account.uid = req_body['uid']
                social_account.provider = provider
                social_account.extra_data = management_api_user
                social_account.save()

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
                    token=remote_authenticated_user[1],
                    token_secret=management_api_jwt,
                    expires_at=expires_at
                    )

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
                    'user_social_auth_id': user_social_auth.id,
                    'account_email_id': account_email.id,
                    'management_user': management_api_user,
                    'social_account_id': social_account.id,
                    'social_app_id': social_app_data.pk,
                    'social_app_name': social_app_data.name,
                    "social_token_id": social_token.id,
                    'association_id': user_association.id,
                    'email_confirmation': True,
                    'user_profile_id': new_userprofile.id,
                }

                data = json.dumps({"DjangoUser": auth_user})
                return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response(ex, content_type='application/json')
