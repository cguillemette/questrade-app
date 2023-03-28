import functools
import logging
import operator

from flask import Flask, abort, jsonify, make_response, request
from flask_cors import CORS

from api.questrade.API import API
from api.questrade.ImplicitOAuthFlow import ImplicitOAuthFlow

application = Flask(__name__, static_folder="./static")
CORS(
    application, 
    resources={r"/*": {"origins": "http://127.0.0.1:3002"}}, 
    supports_credentials=True
    )

log = logging.getLogger(__name__)

@application.errorhandler(429)
def too_many_requests(e):
    return jsonify(error=str(e)), 429

@application.route('/')
def app():
    return application.send_static_file("login.html")

@application.route('/api/accounts')
def api():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    expires_at = request.cookies.get('expires_at')
    api_server = request.cookies.get('api_server')

    flow = ImplicitOAuthFlow(access_token, refresh_token, expires_at, api_server)
    tokens = flow.get_valid_access_token()

    def market_value(element):
        return element['currentMarketValue']

    def total_cost(element):
        return element['totalCost']

    resp = make_response(f"Unexpected error occured.", 400)
    try:
        api = API(tokens['access_token'], tokens['api_server'])
        account_id = api.get_account_id()

        positions = {}
        result_market_value = 0
        result_total_cost = 0
        for _ in account_id:
            account_positions = api.get_account_positions(_)
            positions[_] = account_positions
            log.error(positions)
            result_market_value += functools.reduce(operator.add, map(market_value, positions[_]))
            result_total_cost += functools.reduce(operator.add, map(total_cost, positions[_]))

        resp = make_response(jsonify({
            "accounts": positions,
            "summary": {
                "result_market_value": result_market_value,
                "result_total_cost": result_total_cost
            }}), 200)
    except:
        abort(429, "Try again later.")
    finally:
        resp.set_cookie('access_token', tokens['access_token'])
        resp.set_cookie('refresh_token', tokens['refresh_token'])
        resp.set_cookie('expires_at', tokens['expires_at'])
        resp.set_cookie('api_server', tokens['api_server'])

    return resp