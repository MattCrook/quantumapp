import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile
from rest_auth.models import TokenModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
# from rest_framework.authtoken.models import Token
# from rest_auth.models import DefaultTokenModel



# @csrf_exempt
# @renderer_classes((JSONRenderer))
@api_view(('GET', 'POST'))
def login_user(request):
    try:
        req_body = json.loads(request.body.decode())

        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':
            user = request.user

            if user.email == req_body['email']:
                email = req_body['email']
                password = req_body['password']
                authenticated_user = authenticate(email=email, password=password)

                token = TokenModel.objects.get(user=user)
                login(request, user, backend='django.contrib.auth.backends.RemoteUserBackend')
                session = request.session

                data = json.dumps(
                    {
                        "valid": True,
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "username": user.username,
                        "auth0_identifier": user.auth0_identifier,
                        "QuantumToken": token.key,
                        "session": session.session_key
                    }
                )
                return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False, "Error": 'Unable to Authenticate Credentials'})
            return HttpResponse(data, content_type='application/json')

    except Exception as ex:
        return Response({'message': ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
