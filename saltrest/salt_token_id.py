from saltops2.settings import SALT_USER, SALT_PASSWORD, SALT_REST_URL
from saltrest.salt_https_api import salt_api_token


def token_id():
    s = salt_api_token(
        {
            "username": SALT_USER,
            "password": SALT_PASSWORD,
            "eauth": "pam"
        },
        SALT_REST_URL + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token
