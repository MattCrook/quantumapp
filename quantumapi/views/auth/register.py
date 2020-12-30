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
from jose import jwt
# import requests as req
import json
import datetime
import http.client
from social_django.context_processors import backends
# from social_django.admin import Association, UserSocialAuth
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token


# @csrf_exempt
@api_view(('GET', 'POST'))
def register_user(request):
    try:
        req_body = json.loads(request.body.decode())
        backend = backends(request)
        print("BACKENDS", backends)

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
        # open_id_config = get_open_id_config(req_body['uid'])
        # print("OEPNID", open_id_config)

        login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')

        session_user = request.session
        is_account_email = EmailAddress.objects.filter(user_id=user.id).exists()
        is_session = Session.objects.filter(session_key=session_user.session_key).exists()
        is_user_social_auth = UserSocialAuth.objects.filter(user_id=user.id).exists()

        if is_session:
            session = request.session
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
                issued=iat, lifetime=exp,
                assoc_type=assoc_type
                )


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
        }

        data = json.dumps({"DjangoUser": user_obj})
        return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response(ex, content_type='application/json')



def get_open_id_config(uid):
    conn = http.client.HTTPConnection("https://dev-405n1e6w.auth0.com/api/v2/users/" + uid)
    headers = { 'authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FVkJSRU0wTlRKRFFqa3hRalEyTXpJMVFqbENPVEkzUVRJMU16UTRPRE5HTXpSRVJURkVSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi00MDVuMWU2dy5hdXRoMC5jb20vIiwic3ViIjoiclhDQWJVZ05qV0NiZmxnQWlVVTk3VXV4MWVpWFVOWnVAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZGV2LTQwNW4xZTZ3LmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNjA5MjgyMDY5LCJleHAiOjE2MDkzNjg0NjksImF6cCI6InJYQ0FiVWdOaldDYmZsZ0FpVVU5N1V1eDFlaVhVTlp1IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.LEiimVbRd9S7VvRgpP-5Kp0t8t3ihyeUrL6rqJXXIp8_t5mYIc4xafaq98ZIlIOrTPAvR8ZF_IxejWCKSXkqJ1t_L65lBiXaoLhpCOFGBxoI3daE4RoEEejSKV1AeYcv2ER1qX0sQC0Wfwn6LsVBSI-B_A-NZF6I7mBSIfbtxojXSiV1ampbg9bveDFmU-WNFgeEM6mV_33qJQY0G8mgJGCwXN3w9feD11IUvvnUEdP_JAM2JA-tf6dl23TLDAu8-S90VnnZZJcWRJX8yBlaNnQuDAKZps_rn1BP6_hh7nfj_rQOt2lto6MS0AVog9Zp23jHVmLx-1YAfHPmPRYPhA" }
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
