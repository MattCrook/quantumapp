import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile
from rest_auth.models import TokenModel
from rest_auth.models import DefaultTokenModel
# from rest_framework.authtoken.models import Token




@csrf_exempt
def login_user(request):

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = DefaultTokenModel.objects.get(user=authenticated_user)
            data = json.dumps(
                {
                    "id": authenticated_user.id,
                    "first_name": authenticated_user.first_name,
                    "last_name": authenticated_user.last_name,
                    "email": authenticated_user.email,
                    "username": authenticated_user.username,
                    "auth0_identifier": authenticated_user.auth0_identifier,
                    "QuantumToken": token.key
                }
            )
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

                    # "valid": True,
                    # "user_id": authenticated_user.id,
                    # "token": token.key
