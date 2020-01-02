import os
import json

from six.moves.urllib.request import urlopen
from jose import jwt

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_API_ID = os.environ.get("AUTH0_API_ID")

def verify_token(token):
    # Validate the token to make sure it's authentic
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    # This currently expects the token to have three distinct sections 
    # each separated by a period.
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:  # to validate the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=AUTH0_API_ID,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            print("token validated successfully")
            return payload
        except jwt.ExpiredSignatureError:
            print("Token is expired")
            raise Exception('Unauthorized')
        except jwt.JWTClaimsError:
            print("Token has invalid claims")
            raise Exception('Unauthorized')
        except Exception:
            print("Unable to parse token")
            raise Exception('Unauthorized')
        