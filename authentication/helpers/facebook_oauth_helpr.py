import json
import time
import requests
from django.conf import settings
from django.contrib.auth.models import User
from hashlib import md5
from enum import Enum, unique
from authentication.models import OauthUser


def _build_statement_string():
    current_timestamp = int(time.time())
    signature = md5(f'{settings.FACEBOOK_SIGNATURE_SALT}.{current_timestamp}'.encode('utf-8')).hexdigest()
    statement = {
        'ts': current_timestamp,
        'sig': signature
    }
    return json.dumps(statement)


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
        try:
            self.validate_statement_string()
            return self.get_or_create_user()
        except KeyError:
            raise ValueError("(109) Internal Error: Invalid payload.")

    def de_auth(self):
        """
        deAuth Callback
        ref: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/v2.1#deauth-callback
        :return:
        """
        signed_request = self.params['signed_request']
        encoded_sig, payload = signed_request.split('.')
        # @TODO: validate signature, secret, and decode payload
        # using a sample data here
        decoded_payload = {
            'user_id': 1
        }
        user_id = decoded_payload['user_id']

        try:
            oauth_user = OauthUser.objects.get(uid=user_id)
            oauth_user.user.is_active = False
            oauth_user.user.save()
        except OauthUser.DoesNotExist:
            raise ValueError("(106) Invalid User.")

    def _build_url(self, api_endpoint):
        """
        Build FB request url based on endpoint
        :param api_endpoint:
        :return:
        """
        if not isinstance(api_endpoint, self.ApiEndpoint):
            raise ValueError("(103) Internal Error.")
        return f'{settings.FACEBOOK_GRAPH_API}/{api_endpoint.value}'

    def _get_access_token(self):
        """
        Send API request to FB to get user access token
        example response format:
        {
            "access_token": "EAAE09MykwygBALJM2GvE3Y7IZBJlMAcSZACVw4HRN6Rx9pQ21bq4SwvYZBeP7FHFhLjC124CM2ZBrv7XjDba0ZBliiush3PllZAsUV21VhVYHyk5mH5oBOULEGC6OmjuxauNZCmaIlMJUL43bk4dZBrAxItT6fUwLFEOK4PzziWv0gZDZD",
            "token_type": "bearer",
            "expires_in": 5181249
        }
        :return:
        """
        response = requests.post(self._build_url(self.ApiEndpoint.ACCESS_TOKEN), data={
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_OAUTH_CALLBACK,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': self.params['code']
        }, timeout=settings.OAUTH_REQUEST_TIMEOUT)
        if response.status_code == 200:
            res_data = response.json()
            token_data = {
                'access_token': res_data['access_token'],
                'expires_in': res_data['expires_in'],
                'token_type': res_data['token_type']
            }
            return token_data
        else:
            raise ValueError("(101) Authorization failed, please try again")

    def _get_user_profile_from_FB(self, access_token):
        """
        Send API request to FB to get user FB profile
        example response format:
        {
            "id": "1590431021090935",
            "name": "Claire Yunyun Chen",
            "email": "clairecyyyyy@gmail.com",
            "picture": {
                "data": {
                    "height": 50,
                    "is_silhouette": false,
                    "url": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=1590431021090935&height=50&width=50&ext=1563896086&hash=AeR1wTlXtMaSrWEo",
                    "width": 50
                }
            }
        }
        """
        response = requests.get(self._build_url(self.ApiEndpoint.ME), params={
            'access_token': access_token,
            'fields': 'id,name,email,picture,first_name,last_name',
        }, timeout=settings.OAUTH_REQUEST_TIMEOUT)

        if response.status_code == 200:
            try:
                res_data = response.json()
                user_profile = {
                    'external_id': res_data['id'],  # facebook unique id
                    'first_name': res_data['first_name'],
                    'last_name': res_data['last_name'],
                    'profile_picture': res_data['picture']['data']['url']
                }
                return user_profile
            except ValueError:
                raise ValueError("(102) Bad Facebook response format. Please try again")
        else:
            # @TODO: add error handling for different error code
            raise ValueError("(104) Failed to get user information, please try again")

    def get_or_create_user(self):
        token_data = self._get_access_token()
        user_profile = self._get_user_profile_from_FB(access_token=token_data['access_token'])
        try:
            # if user exists, update the access token and expires time
            oauth_user = OauthUser.objects.get(external_id=user_profile['external_id'])
            oauth_user.access_token = token_data['access_token']
            oauth_user.expires_in = token_data['expires_in']
            oauth_user.save()
            return oauth_user.user
        # if user is new, create user records
        except OauthUser.DoesNotExist:
            user = User.objects.create(
                username=user_profile['email'],
                is_active=True,
                password='',  # this field cannot be None
                first_name=user_profile['first_name'],
                last_name=user_profile['last_name']
            )
            OauthUser.objects.create(
                user=user,
                external_id=user_profile['external_id'],
                access_token=token_data['access_token'],
                token_expires_in=token_data['expires_in'],
                profile_picture=user_profile['user_profile']
            )
            return user

    def validate_statement_string(self):
        """
        Validate statement string from FB response to avoid cross-site attack
        :return:
        """
        statement = json.loads(self.params['state'])
        ts = statement.get('ts', None)
        if ts:
            signature = md5(f'{settings.FACEBOOK_SIGNATURE_SALT}.{ts}'.encode('utf-8')).hexdigest()
            if signature == statement.get('sig'):
                return True
        raise ValueError("(105) Invalid Statement string.")
