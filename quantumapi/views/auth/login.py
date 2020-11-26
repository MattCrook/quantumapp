import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile
from rest_auth.models import DefaultTokenModel
from rest_auth.models import TokenModel
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@csrf_exempt
@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login_user(request):

    print("REMOTEUSER", request.META['USER'])
    try:
        req_body = json.loads(request.body.decode())

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':

            # Use the built-in authenticate method to verify
            email = req_body['email']
            password = req_body['password']
            authenticated_user = authenticate(email=email, password=password)
            print("Login: authUser", authenticated_user)

            # If authentication was successful, respond with their token
            if authenticated_user is not None:
                token = TokenModel.objects.get(user=authenticated_user)
                print("Login: restauthtoken", token)
                data = json.dumps(
                    {
                        "valid": True,
                        "id": authenticated_user.id,
                        "first_name": authenticated_user.first_name,
                        "last_name": authenticated_user.last_name,
                        "email": authenticated_user.email,
                        "username": authenticated_user.username,
                        "auth0_identifier": authenticated_user.auth0_identifier,
                        "QuantumToken": token.key
                    }
                )
                # login(request, authenticated_user)
                return HttpResponse(data, content_type='application/json')

            else:
                # Bad login details were provided. So we can't log the user in.
                data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
                return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
