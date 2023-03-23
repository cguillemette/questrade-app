import logging

from flask import Flask, jsonify, make_response, request

from app.questrade.ImplicitOAuthFlow import ImplicitOAuthFlow

from qtrade import questrade

application = Flask(__name__, static_folder="./static")

log = logging.getLogger()

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

    return jsonify(
        tokens=tokens
    )
