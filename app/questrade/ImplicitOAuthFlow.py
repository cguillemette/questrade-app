import json
import time
import logging
from urllib import request

import requests

CONSUMER_KEY = "hUQAC4GccGaOF4JHGKEb11sI66xm3Q"
REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token={}"

# Step 1) Customer is authorized using the Questrade login url which returns access token and refresh token
# => https://login.questrade.com/oauth2/authorize?client_id=<client id>&response_type=token&redirect_uri=<url>
# Step 2) Upon any calls to API, we refresh token if they expired

log = logging.getLogger(__name__)

class ImplicitOAuthFlow:    
    def __init__(self,
        access_token: str,
        refresh_token: str,
        expires_at: str,
        api_server: str
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.api_server = api_server
        self.refreshed = False

    def __refresh_token(self, refresh_token):
        r = request.urlopen(REFRESH_TOKEN_URL.format(refresh_token))
        if r.getcode() == 200:
            token = json.loads(r.read().decode('utf-8'))
            log.error(token)
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            expires_at = int(time.time()) + int(token['expires_in'])
            self.expires_at = str(expires_at)
            self.api_server = token['api_server']
            self.refreshed = True

    def __tokens(self):
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "api_server": self.api_server,
            "refreshed": self.refreshed
        }

    def get_valid_access_token(self):
        if time.time() > int(self.expires_at):
            self.__refresh_token(self.refresh_token)
        return self.__tokens()
