#!/usr/bin/python3
# -*- coding:utf-8 -*-

import datetime
import fnmatch
import os
import time

from v2 import const as C
from v2.daemons import daemon_logger
from v2.databases.db_redis import RDConnector
from v2.helpers import utils, validator

""" 도메인 수집 프로그램
앱 로그인, 로그아웃시 이메일 정보 지속적으로 갱신하며, 
수집된 이메일 주소만 FCM 알림이 발송된다

앱 로그인, 로그아웃시 /tmp/domain_list 내에 'login_{이메일주소}',
'logout_{이메일주소}' 형식으로 파일이 생성되며, 정보수집후 파일은 즉시 삭제
"""

_rd = RDConnector()

#: 도메인 리스트 원본파일
FCM_DOMAIN_PATH = C.LocalPath.FCM_DOMAIN_LIST

#: 작업경로
TMP_DOMAIN_PATH = "{0}/".format(C.LocalPath.TMP_DOMAIN_LIST)

#: REDIS 사용자키
USER_KEY = C.RedisKey.NOTI_USER

#: Prefix Login
PREFIX_LOGIN = "login_"

#: Prefix Logout
PREFIX_LOGOUT = "logout_"


def run():
    while True:
        try:
            if os.listdir(TMP_DOMAIN_PATH):
                for _file in os.listdir(TMP_DOMAIN_PATH):
                    #: 로그인
                    if fnmatch.fnmatch(_file, "{0}*".format(PREFIX_LOGIN)):
                        email = _file.replace("{0}".format(PREFIX_LOGIN), "")
                        os.remove("{0}{1}".format(TMP_DOMAIN_PATH, _file))

                        _path = utils.get_user_fcm_path(email)
                        if not os.path.isfile(_path):
                            with open(_path, "w") as fd:
                                fd.write(email)
                        else:
                            pass

                    #: 로그아웃 (redis에 키가 완전히 없을때 리스트 삭제처리)
                    elif fnmatch.fnmatch(_file, "{0}*".format(PREFIX_LOGOUT)):
                        email = _file.replace("{0}".format(PREFIX_LOGOUT), "")
                        user_is_exists = chk_key_exists(email)

                        if not user_is_exists:
                            _path = utils.get_user_fcm_path(email)
                            if os.path.isfile(_path):
                                os.unlink(_path)
                            else:
                                pass

                        os.remove("{0}{1}".format(TMP_DOMAIN_PATH, _file))
        except Exception as e:
            daemon_logger.save_log(
                C.Logger.DEXTRACTOR,
                "{0} [RunErr : {1}]".format(datetime.datetime.now(), str(e)),
            )

        time.sleep(5)


def chk_key_exists(email):
    """도메인 키 존재여부 검사"""
    res = True
    conn = _rd.connection

    if conn:
        key = conn.keys("{0}{1}".format(USER_KEY, email))
        res = bool(not validator.data_is_empty(key))

    return res


if __name__ == "__main__":
    run()
