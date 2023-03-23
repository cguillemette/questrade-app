import json
import time
import logging
from urllib import request

import requests

CONSUMER_KEY = "hUQAC4GccGaOF4JHGKEb11sI66xm3Q"
REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token={}"
# Customer is authorized by redirecting to Questrade
# => https://login.questrade.com/oauth2/authorize?client_id=<client id>&response_type=token&redirect_uri=<url>
# Real-life examples:
# https://login.questrade.com/oauth2/authorize?client_id=hUQAC4GccGaOF4JHGKEb11sI66xm3Q&response_type=token&redirect_uri=https://dpjxcb4wla.execute-api.us-east-1.amazonaws.com
# access_token=Tfwjy5ubpwOcXalWpKNJi6_VoFX8U7ck0&refresh_token=A0kyxSmx1lcJOLqBflwaf88dNjBUHdKF0&token_type=Bearer&expires_in=1800&api_server=https://api06.iq.questrade.com/

log = logging.getLogger()

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
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            expires_at = int(time.time()) + int(token['expires_in'][0])
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
