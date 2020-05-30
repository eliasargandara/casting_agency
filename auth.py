import json
from flask import request
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'chad-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'


def get_bearer_token():
    if 'Authorization' not in request.headers:
        raise Unauthorized(
            description='Authorization header is expected.'
        )

    parts = request.headers['Authorization'].split(' ')
    if parts[0].lower() != 'bearer':
        raise Unauthorized(
            description='Authorization header must start with "Bearer".'
        )
    elif len(parts) == 1:
        raise Unauthorized(
            description='Authorization token not found.'
        )
    elif len(parts) != 2:
        raise Unauthorized(
            description='Authorization header must be a bearer token.'
        )

    token = parts[1]
    return token


def get_jwks():
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    return jwks


def find_rsa_key(unverified_header, jwks):
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise Unauthorized(
            description='Authorization malformed.'
        )

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    return rsa_key


def retrieve_rsa_key(unverified_header):
    jwks = get_jwks()
    rsa_key = find_rsa_key(unverified_header, jwks)

    if not rsa_key:
        raise BadRequest(
            description=(
                'Unable to find the appropriate authentication key.'
            )
        )

    return rsa_key


def decode_token(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = retrieve_rsa_key(unverified_header)
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise Unauthorized(
            description='Token expired.'
        )
    except jwt.JWTClaimsError:
        raise Unauthorized(
            description=(
                'Incorrect claims. Please check the audience and issuer.'
            )
        )
    except (jwt.JWTError, jwt.JWSError):
        raise BadRequest(
            description='Unable to parse authentication token.'
        )
    except Exception as exception:
        raise


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise BadRequest(
            description='The token is missing permissions.'
        )

    if permission not in payload['permissions']:
        raise Forbidden(
            description=(
                'The account is not authorized to access this resource.'
            )
        )


def requires_auth(permission=''):
    def requires_auth_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            token = get_bearer_token()
            token_payload = decode_token(token)
            check_permissions(permission, token_payload)
            return function(*args, **kwargs, token=token_payload)
        return wrapper
    return requires_auth_decorator
