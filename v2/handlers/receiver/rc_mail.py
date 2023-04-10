#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast
import json

from v2 import const as C
from v2.handlers.sender.sd_utils import SendUtilHandler
from v2.helpers import log_maker, utils, validator
from v2.models import _md_mail


""" 메일 알림 저장
이메일 수신시 '보낸사람, 제목'으로 구성된 알림데이터 수신하면 
Redis에 큐로 적재한다.
"""

_send_utils = SendUtilHandler()


class MailReceiveHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.RC_MAIL, msg=str(msg))

    def __str__(self):
        return self.msg


class MailReceiveHandler:
    def __init__(self):
        self.pass_list, self.pass_type = _send_utils.get_pass_list()

    def receive_noti(self, data, ip):
        """이메일 수신"""
        try:
            #: 필수검사1 : Payload
            if validator.data_is_empty(data):
                return False

            #: 필수검사2 : Type
            if data["type"] == "organ1" or data["type"] == "user1":
                return False

            data = ast.literal_eval(json.dumps(data))
            email = data.get("to", "")

            #: 필수검사3 : 이메일주소
            if validator.data_is_empty(email):
                return False

            data["log"] = log_maker.make_log_msg(
                ip=ip, email=email, subject=data["subject"]
            )

            data["ip"] = ip

            fcm_valid = self.pre_check_noti(data)
            if fcm_valid:
                #: 메일데이터 Redis 삽입
                _md_mail.put_noti(data)
        except Exception as e:
            raise MailReceiveHandlerException(str(e))

    def pre_check_noti(self, data):
        """메일 큐 적재여부 선검사"""
        email = data["to"]
        is_pass_domain = _send_utils.check_pass_for_domain(email)
        is_pass_ip = _send_utils.check_pass_for_ip(data["ip"])

        #: 1차 검증 > PASS_LIST에 도메인 또는 IP가 존재하는가
        if is_pass_domain or is_pass_ip:
            return True

        #: 2차 검증 > fcm_dom_list에 계정파일이 존재하는가
        return utils.check_valid_user(email)


if __name__ == "__main__":
    mrh = MailReceiveHandler()
