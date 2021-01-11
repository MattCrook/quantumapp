from django.http import HttpResponse, HttpResponseServerError
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from quantumapi.models import UserProfile
from quantumapi.models import User as UserModel
from ..user import UserSerializer
from .login import login_user
from django.middleware.csrf import get_token
from rest_auth.models import TokenModel
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view, renderer_classes
from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmation
from social_django.models import UserSocialAuth, Association
from social_core.pipeline.social_auth import associate_user
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_OPEN_ID_SERVER_URL
import http.client
from social_django.context_processors import backends
from .management_api_services import get_management_api_config, get_management_api_user
from jose import jwt
import datetime
import json
# import requests as req
# from social_django.admin import Association, UserSocialAuth
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token


# @csrf_exempt
@api_view(('GET', 'POST'))
def register_user(request):
    try:
        req_body = json.loads(request.body.decode())
        # backend = backends(request)
        # print("BACKENDS", backends)

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
        authenticated_user = authenticate(email=email, password=password)
        associate_user('django.contrib.auth.backends.RemoteUserBackend', req_body['uid'], user, req_body['provider'])
        # UserModel.blacklistedtoken_set.related_manager_cls.create()
        # UserModel.socialaccount_set.related_manager_cls.create()

        token = TokenModel.objects.create(user=user)
        key = token.key
        csrf = get_token(request)
        provider = req_body['provider']
        extra_data = req_body['extra_data']
        id_token = json.loads(req_body['id_token'])
        nonce = id_token['nonce']
        exp = id_token['exp']
        iat = id_token['iat']
        assoc_type = "Username-Password-Authentication"

        login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')

        session_user = request.session
        is_account_email = EmailAddress.objects.filter(user_id=user.id).exists()
        is_session = Session.objects.filter(session_key=session_user.session_key).exists()
        is_user_social_auth = UserSocialAuth.objects.filter(user_id=user.id).exists()

        if is_session:
            session = Session.objects.get(session_key=session_user.session_key)
            session.save()
        else:
            session = Session.objects.create(user=user)
            session.save()

        if is_account_email:
            account_email= EmailAddress.objects.get(email_address=user.email)
        else:
            account_email = EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,
                primary=True
                )
            email_confirmation = EmailConfirmation.objects.create(
                email_address=account_email,
                key=key,
                sent=datetime.datetime.now()
                )

        if is_user_social_auth:
            user_social_auth = UserSocialAuth.get_user(req_body['uid'])
        else:
            user_social_auth = UserSocialAuth.objects.create(user=user, uid=req_body['uid'], provider=provider, extra_data=extra_data)
            server_url = AUTH0_OPEN_ID_SERVER_URL + req_body['uid']
            user_association = Association.objects.create(
                server_url=server_url,
                handle='social_django',
                secret=AUTH0_CLIENT_SECRET,
                issued=iat,
                lifetime=exp,
                assoc_type=assoc_type
                )
            # social_user = UserSocialAuth.create_social_auth(user, user.id, 'quantummanagement')
            # credential = {
            #     'username': user.username,
            #     'password': user.password,
            # }
            # credentials = CredentialsModel(user=user, credentials=credential)
            # django_token = Token.objects.get(user=user)

            # extra_data = {
            #     "token": django_token.key,
            #     # "credentials": credentials,
            # }
            # social_user.extra_data = extra_data
            # social_user.save()
            # credentials.save()

        management_token = get_management_api_config(AUTH0_DOMAIN)
        management_api_token = json.loads(management_token)
        management_api_jwt = management_api_token['access_token']
        management_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])

        user_obj = {
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
            'management_user': management_user,
        }

        data = json.dumps({"DjangoUser": user_obj})
        return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response(ex, content_type='application/json')
