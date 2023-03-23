import json
import time
from urllib import request

import requests

REFRESH_TOKEN_URL = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="

class Questrade:    
    def __init__(self,
        access_token: str,
        refresh_token: str,
        expires_in: str
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.expires_at = None

    def __refresh_token(self, refresh_token):
        req_time = int(time.time())
        r = request.urlopen(REFRESH_TOKEN_URL.format(refresh_token))
        if r.getcode() == 200:
            token = json.loads(r.read().decode('utf-8'))
            self.expires_at = str(req_time + token['expires_in'])
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']

    def get_valid_access_token(self):
        if time.time() + self.expires_in < int(self.expires_at):
            return self.access_token
        else:
            self.__refresh_token(self.refresh_token)
            return self.access_token
