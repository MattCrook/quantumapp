from functools import wraps
from urllib import request
from jose import jwt
from social_core.backends.open_id import BaseOAuth2
from django.http import JsonResponse
# from social_core.backends.oauth import BaseOAuth2
# import jwt



# Obtains the Access Token from the Authorization Header
def get_token_auth_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]
    return token


# Determines if the required scope is present in the Access Token
# Args: required_scope (str): The scope required to access the resource
def requires_scope(required_scope):
    print("scopeprint", required_scope)
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            print(args)
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse(
                {'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope



class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('picture', 'picture'),
        ('email', 'email')
    ]

    def authorization_url(self):
        return 'https://' + self.setting('DOMAIN') + '/authorize'

    def access_token_url(self):
        return 'https://' + self.setting('DOMAIN') + '/oauth/token'

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get('id_token')
        jwks = request.urlopen('https://' + self.setting('DOMAIN') + '/.well-known/jwks.json')
        issuer = 'https://' + self.setting('DOMAIN') + '/'
        print('{In Auth0 Backend}', issuer)
        audience = self.setting('KEY')  # CLIENT_ID
        payload = jwt.decode(id_token, jwks.read(), algorithms=['RS256'], audience=audience, issuer=issuer)
        strategy = self.strategy
        print("get_user_details: Auth0 Backend", strategy)

        return {'username': payload['nickname'],
                'name': payload['name'],
                'picture': payload['picture'],
                'user_id': payload['sub'],
                'email': payload['email']}





# class Auth0OpenID(OpenIDAuth):
#     name = 'auth0'






# Adding public and private endpoints.
# The @api_view decorator can be added to all endpoints that indicate that the method requires authentication.
# Lastly, the @permission_classes([AllowAny]) can be added to the public endpoint(s) to accept unauthenticated requests.

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def public(request):
#     return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


# @api_view(['GET'])
# def private(request):
#     return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


# # Use the requires_scope decorator in the methods that require specific scopes granted. 
# # The method below requires the read:messages scope granted.
# @api_view(['GET'])
# @requires_scope('read:messages')
# def private_scoped(request):
#     return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})
