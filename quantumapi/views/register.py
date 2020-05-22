import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from quantumapi.models import UserProfile


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        username=req_body['username'],
        password=req_body['password'],
        email=req_body['email']
    )

    userprofile = UserProfile.objects.create(
        rollerCoaster_credits=req_body['rollerCoaster_credits'],
        address=req_body['address'],
        user=new_user
    )

    # Commit the user to the database by saving it
    userprofile.save()
    # userprofile.save_userProfile()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # token = Token.objects.create_userProfile(user=userprofile)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')


# def jwt_create_response_payload(token, user=None, request=None, issued_at=None):
#     """
#     Return data ready to be passed to serializer.

#     Override this function if you need to include any additional data for
#     serializer.

#     Note that we are using `pk` field here - this is for forward compatibility
#     with drf add-ons that might require `pk` field in order (eg. jsonapi).
#     """

#     response_payload = namedtuple('ResponsePayload', 'pk token user')
#     response_payload.pk = issued_at
#     response_payload.token = token
#     response_payload.user = user

#     return response_payload
##############################

# Creating new Toke Manually
# from rest_framework_jwt.settings import api_settings

# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# payload = jwt_payload_handler(user)
# token = jwt_encode_handler(payload)

###############################

# Extending / Overiding
# Right now JSONWebTokenAuthentication assumes that the JWT will come in the header, or a cookie if configured (JWS_AUTH_COOKIE)
# CAn also come in query string, so can write a custom Authentication class

# class JSONWebTokenAuthenticationQS(JSONWebTokenAuthentication):

#     def get_jwt_value(self, request):
#         return request.QUERY_PARAMS.get('jwt')
