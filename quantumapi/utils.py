from django.contrib.auth import authenticate
import json
import jwt
import requests
import os
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN


# function that maps the sub field from the access_token to the username.
# Then, the authenticate method from RemoteUserBackend will create a remote user in the Django authentication system and return a User object for the username.
def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


# function to fetch the JWKS from Auth0 account to verify and decode the incoming Access Token.
def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-405n1e6w.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('dev-405n1e6w.auth0.com')
    return jwt.decode(token, public_key, audience=API_IDENTIFIER, issuer=issuer, algorithms=['RS256'])
