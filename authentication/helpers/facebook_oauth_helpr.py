import json
import time
from django.conf import settings
from hashlib import md5
from enum import Enum, unique

def oauth_login_url():
    return f'{settings.FACEBOOK_OAUTH_URL}?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_OAUTH_CALLBACK}&state={_build_statement_string()}&scope=email'


class FacebookOauthHelper(object):
    @unique
    class ApiEndpoint(Enum):
        ME = 'me'
        ACCESS_TOKEN = 'oauth/access_token'

    def __init__(self, params):
        self.params = params

    def authorize(self):
        """
        FB authorize callback
        validate statement string, find or create user record in the system and return
        :return: 
        """
        pass

    def de_auth(self):
        """
        deAuth Callback
        ref: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/v2.1#deauth-callback
        :return:
        """
        pass
