#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast
import json

from v2 import const as C
from v2.helpers import log_maker, utils, validator
from v2.models import _md_outsider

""" 웹훅 알림 등록
Jandi등 유사 웹훅서비스가 존재하면 본 프로그램에 수신주소를 등록할 수 있다.
반대로 웹훅을  삭제할 수 있다.
"""


class OutsiderReceiveHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.RC_OUTSIDER, msg=str(msg))

    def __str__(self):
        return self.msg


class OutsiderReceiveHandler:
    def __init__(self):
        pass

    def receive_webhook(self, data):
        """웹훅 수신"""
        if validator.data_is_empty(data):
            return False

        data = ast.literal_eval(json.dumps(data))

        wh_data = data[0]
        wh_type = wh_data["hook_type"]

        if wh_type == "post" or wh_type == "put":
            self.post_webhook(wh_data)
        elif wh_type == "del":
            self.delete_webhook(wh_data)

    def post_webhook(self, data):
        """웹훅 추가/수정"""
        hook_data = {
            "wh_dom": data["an_email"],
            "wh_host": data["an_data"]["host"],
            "wh_curl": data["an_hook_curl"],
            "wh_token": data["an_token"],
        }

        _md_outsider.post_webhook(hook_data)

    def delete_webhook(self, data):
        """웹훅 삭제"""
        uuid_arr = utils.split_text(data["an_uuid"], "_", -1)
        hook_data = {
            "wh_dom": data["an_email"],
            "wh_uuid": "{0}_{1}".format(uuid_arr[2], uuid_arr[3]),
        }

        _md_outsider.delete_webhook(hook_data)


if __name__ == "__main__":
    orh = OutsiderReceiveHandler()
