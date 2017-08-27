from saltjob.salt_https_api import salt_api_token
from saltops.settings import SALT_OPS_CONFIG


def token_id():
    s = salt_api_token(
        {
            "username": SALT_OPS_CONFIG['salt_api_user'],
            "password": SALT_OPS_CONFIG['salt_api_password'],
            "eauth": "pam"
        },
        SALT_OPS_CONFIG['salt_api_url'] + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token
