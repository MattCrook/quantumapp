from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile
from rest_auth.models import TokenModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.sessions.models import Session
from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmation
from social_django.models import UserSocialAuth, Association
from .management_api_services import get_management_api_config, get_management_api_user

from social_django.views import auth, do_auth
from social_django.context_processors import backends

from social_core.pipeline.social_auth import associate_user
from django.middleware.csrf import get_token
from quantumapp.settings import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_OPEN_ID_SERVER_URL
from jose import jwt
import json
import datetime



@api_view(('GET', 'POST'))
def login_user(request):
    try:
        req_body = json.loads(request.body.decode())

        if request.method == 'POST':
            user = request.user

            if user.email == req_body['email']:
                email = req_body['email']
                password = req_body['password']
                authenticated_user = authenticate(email=email, password=password)
                associate_user('django.contrib.auth.backends.RemoteUserBackend', req_body['uid'], user, req_body['provider'])

                token = TokenModel.objects.get(user=user)

                if token is not None:
                    token = TokenModel.objects.get(user=user)
                else:
                    token = TokenModel.objects.create(user=user)

                extra_data = req_body['id_token']
                provider = req_body['provider']
                key = token.key
                provider = req_body['provider']
                extra_data = req_body['extra_data']
                id_token = json.loads(req_body['id_token'])
                nonce = id_token['nonce']
                exp = id_token['exp']
                iat = id_token['iat']
                assoc_type = "Username-Password-Authentication"

                if 'csrf_token' in req_body and req_body['csrf_token']:
                    csrf = req_body['csrf_token']
                else:
                    csrf = get_token(request)

                login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')

                session_user = request.session
                is_session = Session.objects.filter(session_key=session_user.session_key).exists()
                is_account_email = EmailAddress.objects.filter(user_id=user.id).exists()
                is_user_social_auth = UserSocialAuth.objects.filter(user_id=user.id).exists()

                try:
                    if is_session:
                        session = Session.objects.get(session_key=session_user.session_key)
                        session.save()
                    else:
                        session = request.session
                        session.save()

                    if is_account_email:
                            account_email = EmailAddress.objects.get(user_id=user.id)
                    else:
                        account_email = EmailAddress.objects.create(
                            user=user,
                            email=user.email,
                            verified=True,
                            primary=True
                            )
                        email_confirmation = EmailConfirmation.objects.create(
                            email_address=account_email,
                            key=request.auth,
                            sent=datetime.datetime.now()
                            )

                    # Get social auth login for user
                    if is_user_social_auth:
                        user_social_auth = UserSocialAuth.objects.get(uid=req_body['uid'])
                        server_url = AUTH0_OPEN_ID_SERVER_URL + req_body['uid']
                        user_association = Association.objects.get(server_url=server_url)
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

                    management_token = get_management_api_config(AUTH0_DOMAIN)
                    management_api_token = json.loads(management_token)
                    management_api_jwt = management_api_token['access_token']
                    management_user = get_management_api_user(AUTH0_DOMAIN, management_api_jwt, req_body['uid'])

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
                            'user_association': user_association.id,
                            'user_social_auth': user_social_auth.id,
                            'account_email': account_email.id,
                            'management_user': management_user,
                            'email_confirmation': True,
                        }

                    data = json.dumps(auth_user)
                    return HttpResponse(data, content_type='application/json')
                except Exception as ex:
                    return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                data = json.dumps({"valid": False, "Error": 'Email did not match email we have for this accout.'})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as ex:
        return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
