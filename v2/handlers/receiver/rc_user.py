#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast
import json
import os

from v2 import const as C
from v2.helpers import log_maker, noti_launcher, responser, utils, validator
from v2.models import _md_user_psql, _md_user_redis


""" 사용자 처리기
사용자가 모바일 및 기타 알림받을 엔드포인트에서 로그인하면 알림서버에 UUID등 고유번호를 등록하며,
차후에 이 고유번호를 가지고 FCM 발송이 이루어진다.
반대로 해제도 가능하다.
"""

# TMP 도메인 경로
TMP_DOMAIN_PATH = C.LocalPath.TMP_DOMAIN_LIST

# Responser
_resp = responser.Responser()


class UserReceiveHandlerException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.RC_USER, msg=str(msg))

    def __str__(self):
        return self.msg


class UserReceiveHandler:
    def __init__(self):
        pass

    """
    사용자 IN / OUT 처리
    * 신규 네이티브 기기
    """

    def receive_mobile_user_login(self, data):
        """사용자 로그인(네이티브 기기 전용)"""
        if validator.data_is_empty(data):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        #: 필수값 검증
        if not validator.login_data_is_valid(data):
            return _resp.Resp(C.ResponseCode.DATA_INSUFFICIENT)

        #: OS종류 검증
        if not validator.os_kind_is_valid(data["osKind"]):
            return _resp.Resp(C.ResponseCode.FIELD_INVALID)

        #: 기준 이메일
        an_email = data.get("email", "")

        if validator.data_is_empty(an_email):
            return _resp.Resp(C.ResponseCode.KEY_INVALID)

        #: PSQL
        users = _md_user_psql.put_user_from_mobile(an_email, data)

        #: Redis
        resp = _md_user_redis.put_user(an_email, users)

        #: File Make
        os.system("touch {0}/login_{1}".format(TMP_DOMAIN_PATH, an_email))

        #: Logger
        log_maker.logging_users(
            msg="[NV] USER LOGIN",
            email=an_email,
            os=data.get("osKind", "UNKNOWN"),
            uuid=data.get("uuid", "UNKNOWN"),
            host=data.get("host", "UNKNOWN"),
        )

        return resp

    def receive_mobile_user_logout(self, data):
        """사용자 로그아웃(네이티브 기기 전용)"""
        if validator.data_is_empty(data):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        if not validator.logout_data_is_valid(data):
            return _resp.Resp(C.ResponseCode.DATA_INSUFFICIENT)

        an_uuid = utils.device_uuid_maker(data["uuid"], data.get("appKind", ""))

        if not an_uuid:
            return False

        del_data = {
            "an_email": data["email"],
            "an_uuid": an_uuid,
            "an_type": data["osKind"],
        }

        return self.receive_remove_user(del_data)

    def make_setting_resp(self, _s):
        """설정 작업 후, 데이터 Resp 재정리"""
        if validator.data_is_empty(_s):
            return {}

        all_settings = _s["au_all"]
        board_settings = _s["au_board"]

        return {
            "email": _s["an_email"],
            "uuid": _s["an_uuid"].replace(C.PostFix.NATIVE_POSTFIX, ""),
            "notifyAll": {
                "mail": all_settings["mail"],
                "eas": all_settings["eas"],
                "board": all_settings["board"],
                "cal": all_settings["cal"],
            },
            "doNotDisturbTime": _s["au_time"],
            "excludeMail": _s["au_mail"],
            "excludeEas": _s["au_eas"],
            "excludeCal": _s["au_cal"],
            "board": {
                "excludeFolders": board_settings["excludeFolders"],
                "notifyToMe": {
                    "comment": board_settings["notifyToMe"]["comment"],
                    "reply": board_settings["notifyToMe"]["reply"],
                },
            },
        }


if __name__ == "__main__":
    urh = UserReceiveHandler()
