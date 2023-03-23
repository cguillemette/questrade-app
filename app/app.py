import logging

from flask import Flask, jsonify, request, send_file, abort, Response

from logging.config import dictConfig

application = Flask(__name__, static_folder="./static")

@application.route('/')
def app():
    return application.send_static_file("login.html")

    # return jsonify(
    #     status=True,
    #     data=_balance
    # )