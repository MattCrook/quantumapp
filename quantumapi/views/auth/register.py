import json
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile, Image, ImageForm
from quantumapi.models import User as UserModel
from ..user import UserSerializer
from .login import login_user
from django.middleware.csrf import get_token
from rest_auth.models import TokenModel
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view, renderer_classes

# from rest_framework.authtoken.models import Token


# @csrf_exempt
@api_view(('GET', 'POST'))
def register_user(request):
    try:
        req_body = json.loads(request.body.decode())

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

        # password already defined above
        # password = req_body['password']
        email = req_body['email']
        authenticated_user = authenticate(email=email, password=password)
        token = TokenModel.objects.create(user=user)
        key = token.key
        login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')
        session_user = request.session
        is_session = Session.objects.filter(session_key=session_user.session_key).exists()
        if is_session:
            session = is_session
        else:
            session = request.session


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
        }

        data = json.dumps({"DjangoUser": user_obj})
        return HttpResponse(data, content_type='application/json')

    except Exception as x:
        return HttpResponse(x, content_type='application/json')
