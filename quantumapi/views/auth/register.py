import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer
from rest_auth.utils import default_create_token
# from rest_auth.views import django_login
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile, Image, ImageForm, User
from ..user import UserSerializer
from .login import login_user
from rest_framework.authtoken.models import Token

# from allauth.account.forms import LoginForm
# from rest_auth.app_settings import DefaultTokenSerializer
# from rest_auth.models import DefaultTokenModel



def register_user(request):

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        new_user = User.objects.create_user(
            first_name=req_body['first_name'],
            last_name=req_body['last_name'],
            username=req_body['username'],
            email=req_body['email'],
            password=req_body['password'],
            auth0_identifier=req_body['auth0_identifier']
        )

        new_userprofile = UserProfile.objects.create(
            address=req_body["address"],
            user=new_user
        )

        # Commit the user to the database by saving it
        new_userprofile.save()

        # Login the newly created user to register with admin site, create a session, and return the user dict and token
        email = req_body['email']
        password = req_body['password']
        authenticated_user = authenticate(email=email, password=password)

        if authenticated_user is not None:
            # Use the REST_AUTH'S token generator on the new user account
            # token = DefaultTokenModel.objects.create(user=new_user)
            # token = default_create_token(TokenModel, authenticated_user, TokenSerializer)
            # key = token.key
            token = Token.objects.create(user=new_user)
            key = token.key

            user_obj = {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "username": new_user.username,
                "is_staff": new_user.is_staff,
                "auth0_identifier": new_user.auth0_identifier,
                "QuantumToken": key
            }

            # Return the response object of choice (with the token) to the client
            data = json.dumps({"DjangoUser": user_obj})
            login(request, authenticated_user)
            return HttpResponse(data, content_type='application/json')

    except Exception as x:
        return HttpResponse(x, content_type='application/json')
