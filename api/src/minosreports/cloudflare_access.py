# The Application Audience (AUD) tag for your application
import datetime
import json
import os
from dataclasses import dataclass

import jwt
import requests
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from jwt.algorithms import RSAAlgorithm

POLICY_AUD = os.getenv("CF_POLICY_AUD")

# Your CF Access team domain
TEAM_DOMAIN = os.getenv("CF_TEAM_DOMAIN")
CERTS_URL = f"{TEAM_DOMAIN}/cdn-cgi/access/certs"

PUBLIC_KEYS_REFRESH_INTERVAL_SECONDS = 3600  # refresh public keys interval


class InvalidTokenError(Exception):
    pass


@dataclass(kw_only=True)
class PublicKeyData:
    public_keys: list[RSAPublicKey]
    public_keys_refresh: datetime.datetime | None


PUBLIC_KEY_DATA = PublicKeyData(public_keys=[], public_keys_refresh=None)


def _get_public_keys():
    """
    Returns:
        List of RSA public keys usable by PyJWT.
    """
    now = datetime.datetime.now(datetime.UTC)
    if (
        PUBLIC_KEY_DATA.public_keys_refresh
        and (PUBLIC_KEY_DATA.public_keys_refresh - now).total_seconds()
        <= PUBLIC_KEYS_REFRESH_INTERVAL_SECONDS
    ):
        return
    PUBLIC_KEY_DATA.public_keys_refresh = now
    resp = requests.get(CERTS_URL, timeout=10)
    PUBLIC_KEY_DATA.public_keys.clear()
    jwk_set = resp.json()
    for key_dict in jwk_set["keys"]:
        public_key = RSAAlgorithm.from_jwk(json.dumps(key_dict))
        if not isinstance(public_key, RSAPublicKey):
            raise Exception("Invalid RSA public key")
        PUBLIC_KEY_DATA.public_keys.append(public_key)


def verify_token(cf_authorization: str):
    _get_public_keys()
    # Loop through the keys since we can't pass the key set to the decoder
    valid_token = False
    for key in PUBLIC_KEY_DATA.public_keys:
        try:
            # decode returns the claims that has the email when needed
            return jwt.decode(
                cf_authorization,
                key=key,
                audience=POLICY_AUD,
                algorithms=["RS256"],
            )
        except:  # noqa: E722, S110
            pass
    if not valid_token:
        raise InvalidTokenError()
