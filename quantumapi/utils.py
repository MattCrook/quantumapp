from django.contrib.auth import authenticate
import json
import jwt
import requests
import os
from quantumapp.settings import API_IDENTIFIER, AUTH0_DOMAIN



def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


# function to fetch the JWKS from Auth0 account to verify and decode the incoming Access Token.
def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    auth0_domain = os.environ.get(AUTH0_DOMAIN)
    print("AUTHODOMAIN", auth0_domain)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(auth0_domain)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    api_identifier = os.environ.get(API_IDENTIFIER)
    print("APIIDENTIFIR", api_identifier)
    issuer = 'https://{}/'.format(auth0_domain)
    return jwt.decode(token, public_key, audience=api_identifier, issuer=issuer, algorithms=['RS256'])
