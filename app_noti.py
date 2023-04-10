#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from v2 import const as C
from v2 import xeno
from v2.helpers import config_loader as _cf
from v2.helpers import log_maker

""" Description
프로그램의 시작점이다.
제일 먼저 URL Routing을 받아 각각 분배기로 전달
"""

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

#: EndPoint Key
ep = C.EndPoint


class RoutingException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.XENO, msg=str(msg))

    def __str__(self):
        return self.msg


@app.route("/notify", methods=["GET", "POST"], endpoint=ep.MAIL)
@app.route("/notify_cal", methods=["GET", "POST"], endpoint=ep.CALENDAR)
@app.route("/domain_change", methods=["GET", "POST"], endpoint=ep.DOMAIN)
@app.route("/handle_mailinfo", methods=["GET", "POST"], endpoint=ep.MAIL_HOST)
@app.route("/put", methods=["GET", "POST"], endpoint=ep.USER_LOGIN)

def route():
    """Routing"""
    r_data = r_ip = ""
    r_path = request.path

    try:
        if (
            request.method == "POST"
            and request.headers
            and "X-Forward-For" in request.headers
        ):
            r_ip = request.headers.getlist("X-Forward-For")[0]

        r_data = request.get_json(silent=True)
    except Exception as e:
        msg = "Routing Exception : ROUTING PATH : {0}, EXCEPT : {1}".format(
            r_path, str(e)
        )
        raise RoutingException(msg)

    return "", 204


if __name__ == "__main__":
    access_info = _cf.get_config(C.ConfigKey.APP)

    host = access_info["app_host"]
    port = access_info["app_port"]

    app.run(host=host, port=int(port))
