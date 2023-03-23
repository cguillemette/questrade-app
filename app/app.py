import logging

from flask import Flask, jsonify, request, send_file, abort, Response

from logging.config import dictConfig

application = Flask(__name__, static_folder="./static")

@application.route('/')
def app():
    return application.send_static_file("login.html")

@application.route('/api')
def api():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    expires_in = request.cookies.get('expires_in')

    return jsonify(
        status=True,
        data=access_token
    )
