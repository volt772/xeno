#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix

from v2 import const as C
from v2 import xeno
from v2.helpers import config_loader as _cf
from v2.helpers import log_maker

""" AppNoti (라우팅)
- Routing URL을 받아 'xeno' 로 전달한다.
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
