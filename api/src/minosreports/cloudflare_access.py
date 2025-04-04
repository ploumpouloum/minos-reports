# The Application Audience (AUD) tag for your application
import os
import requests
import jwt
import json
from jwt.algorithms import RSAAlgorithm, RSAPublicKey
import datetime

POLICY_AUD = os.getenv("CF_POLICY_AUD")

# Your CF Access team domain
TEAM_DOMAIN = os.getenv("CF_TEAM_DOMAIN")
CERTS_URL = f"{TEAM_DOMAIN}/cdn-cgi/access/certs"


class InvalidTokenError(Exception):
    pass


public_keys: list[RSAPublicKey] = []
public_keys_refresh: datetime.datetime | None = None


def _get_public_keys():
    """
    Returns:
        List of RSA public keys usable by PyJWT.
    """
    global public_keys_refresh
    global public_keys
    now = datetime.datetime.now(datetime.UTC)
    if public_keys_refresh and (public_keys_refresh - now).total_seconds() <= 3600:
        return
    public_keys_refresh = now
    print("Refreshing public keys")
    resp = requests.get(CERTS_URL, timeout=10)
    public_keys.clear()
    jwk_set = resp.json()
    for key_dict in jwk_set["keys"]:
        public_key = RSAAlgorithm.from_jwk(json.dumps(key_dict))
        if not isinstance(public_key, RSAPublicKey):
            raise Exception("Invalid RSA public key")
        public_keys.append(public_key)


def verify_token(cf_authorization: str):
    _get_public_keys()
    # Loop through the keys since we can't pass the key set to the decoder
    valid_token = False
    for key in public_keys:
        try:
            # decode returns the claims that has the email when needed
            return jwt.decode(
                cf_authorization,
                key=key,
                audience=POLICY_AUD,
                algorithms=["RS256"],
            )
        except:
            pass
    if not valid_token:
        raise InvalidTokenError()
