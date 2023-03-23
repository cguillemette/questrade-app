import logging

from flask import Flask, jsonify, make_response, request

from app.questrade.API import API
from app.questrade.ImplicitOAuthFlow import ImplicitOAuthFlow

application = Flask(__name__, static_folder="./static")

log = logging.getLogger(__name__)

@application.route('/')
def app():
    return application.send_static_file("login.html")

@application.route('/api')
def api():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    expires_at = request.cookies.get('expires_at')
    api_server = request.cookies.get('api_server')

    flow = ImplicitOAuthFlow(access_token, refresh_token, expires_at, api_server)
    tokens = flow.get_valid_access_token()

    resp = make_response(tokens)
    resp.set_cookie('access_token', tokens['access_token'])
    resp.set_cookie('refresh_token', tokens['refresh_token'])
    resp.set_cookie('expires_at', tokens['expires_at'])
    resp.set_cookie('api_server', tokens['api_server'])

    api = API(access_token, api_server)
    account_ids = api.get_account_id()

    return jsonify(
        tokens=tokens,
        account_ids=account_ids
    )
