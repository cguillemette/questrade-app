# noqa: D103

import functools
import logging
import operator
import os

from flask import Flask, abort, jsonify, make_response, request
from flask_cors import CORS
from dotenv import load_dotenv


try:
    from backend.questrade.API import API
    from backend.questrade.ImplicitOAuthFlow import ImplicitOAuthFlow
except:  # noqa: E722
    from questrade.API import API
    from questrade.ImplicitOAuthFlow import ImplicitOAuthFlow

load_dotenv()

cors_origin_local = os.getenv("CORS_ORIGIN_LOCAL")
cors_origin_questrade_callback = os.getenv("CORS_ORIGIN_QUESTRADE_CALLBACK")
origin_questrade_client_id = os.getenv("QUESTRADE_CLIENT_ID")

app = Flask(__name__, static_folder="./static")
CORS(
    app,
    resources={r"/*": {"origins": [cors_origin_local, cors_origin_questrade_callback]}},
    supports_credentials=True,
)

log = logging.getLogger(__name__)


@app.route("/api/settings", methods=["GET"])
def settings():
    return {
        "cors_origin_local": cors_origin_local,
        "cors_origin_questrade_callback": cors_origin_questrade_callback,
        "origin_questrade_client_id": origin_questrade_client_id,
    }


@app.route("/api/questrade/login/", methods=["GET"])
def questrade_client_id():
    url = (
        f"https://login.questrade.com/oauth2/authorize?"
        f"client_id={origin_questrade_client_id}&"
        f"response_type=token&redirect_uri={cors_origin_questrade_callback}"
    )
    return make_response(
        jsonify(
            {
                "url": url,
            }
        ),
        200,
    )


@app.route("/api/accounts", methods=["POST"])
def accounts():
    body = None
    access_token = None
    refresh_token = None
    expires_at = None
    api_server = None

    try:
        body = request.get_json()

        # Upon login body will be provided. Otherwise, will be provided through cookies.
        access_token = body.get("access_token")
        refresh_token = body.get("refresh_token")
        expires_at = body.get("expires_at")
        api_server = body.get("api_server")
        if (
            access_token is None
            or refresh_token is None
            or expires_at is None
            or api_server is None
        ):
            access_token = request.cookies.get("access_token")
            refresh_token = request.cookies.get("refresh_token")
            expires_at = request.cookies.get("expires_at")
            api_server = request.cookies.get("api_server")
            if (
                access_token is None
                or refresh_token is None
                or expires_at is None
                or api_server is None
            ):
                return abort(401, "Unauthorized")
    except Exception as e:
        log.error(str(e))
        return abort(401, "Failed authorize")

    try:
        tokens = ImplicitOAuthFlow(
            access_token, refresh_token, expires_at, api_server
        ).get_valid_access_token()
    except Exception as e:
        log.error(str(e))
        resp = make_response("Unexpected error occured.", 500)
        return resp

    def market_value(element):
        return element["currentMarketValue"]

    def total_cost(element):
        return element["totalCost"]

    try:
        api = API(tokens["access_token"], tokens["api_server"])
        account_id = api.get_account_id()

        positions = {}
        result_market_value = 0
        result_total_cost = 0
        for _ in account_id:
            account_positions = api.get_account_positions(_)
            positions[_] = account_positions
            result_market_value += functools.reduce(
                operator.add, map(market_value, positions[_])
            )
            result_total_cost += functools.reduce(
                operator.add, map(total_cost, positions[_])
            )

        resp = make_response(
            jsonify(
                {
                    "accounts": positions,
                    "summary": {
                        "result_market_value": result_market_value,
                        "result_total_cost": result_total_cost,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        log.error(e)
        resp = make_response("Unexpected error occured.", 500)
    finally:
        resp.set_cookie("access_token", tokens["access_token"])
        resp.set_cookie("refresh_token", tokens["refresh_token"])
        resp.set_cookie("expires_at", tokens["expires_at"])
        resp.set_cookie("api_server", tokens["api_server"])

    return resp
