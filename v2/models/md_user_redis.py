#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast

from v2 import const as C
from v2.databases.db_redis import RDConnector
from v2.helpers import log_maker, responser, utils, validator

""" 사용자 처리기
사용자가 모바일 및 기타 알림받을 엔드포인트에서 로그인하면 알림서버에 UUID등 고유번호를 등록하며,
차후에 이 고유번호를 가지고 FCM 발송이 이루어진다.
반대로 해제도 가능하다.
"""

_rd = RDConnector()

#: 사용자 정보 키
USER_KEY = C.RedisKey.NOTI_USER

# Responser
_resp = responser.Responser()


class UserRedisModelException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.MD_USER_REDIS, msg=str(msg))

    def __str__(self):
        return self.msg


class UserRedisModel:
    def __init__(self):
        pass

    def get_device_info(self, an_email):
        """기기정보 가져오기"""
        if validator.data_is_empty(an_email):
            return False

        conn = _rd.connection

        if conn:
            token_list = {}

            try:
                lists = utils.hget_to_json(conn.hgetall(USER_KEY + an_email))

                if lists:
                    device_str = lists["deviceInfo"]
                    devices = ast.literal_eval(device_str)

                    for device in devices:
                        token_list[device] = devices[device]
            except Exception:
                pass

            return token_list

    def put_user(self, an_email, data, raw_data=None):
        """사용자 저장
        - 로그인 후, 기기데이터 저장
        - PSQL 삽입후, 삽입데이터 토대로 Redis정보 재갱신
        """
        result = False
        if data:
            self.del_user(an_email)
            result = self.insert_redis_data(an_email, data, raw_data)

        return result

    def del_user(self, email, data=None):
        """사용자 삭제
        - 로그아웃 후, 기기데이터 삭제
        - PSQL 제거후, 잔여데이터 토대로 Redis정보 재갱신
        """
        resp = _resp.Resp(C.ResponseCode.SUCCESS)
        if validator.data_is_empty(email):
            return _resp.Resp(C.ResponseCode.NO_DATA)

        conn = _rd.connection

        if conn:
            conn.delete(USER_KEY + email)

            if data:
                resp = self.insert_redis_data(email, data)

        return resp


    def insert_redis_data(self, email, data, raw_data=None):
        """로그인후, PSQL 데이터 가공 후, 레디스 저장"""
        if validator.data_is_empty(email):
            return False

        conn = _rd.connection

        if conn and email and data:
            n_type = {}
            try:
                for dev in data:
                    #: Native, Hybrid 공통 설정키
                    settings = dev["nu_data"]

                    n_type[dev["nu_uuid"]] = {
                        "an_type": dev["nu_type"],
                        "an_email": dev["nu_email"],
                        "an_token": dev["nu_token"],
                        "an_uuid": dev["nu_uuid"],
                    }

                    if dev["nu_uuid"].endswith("vh_task"):
                        n_type[dev["nu_uuid"]]["au_host"] = settings["host"]
                        pass
                    else:
                        n_type[dev["nu_uuid"]]["au_mail"] = settings["au_mail"]
                        n_type[dev["nu_uuid"]]["au_eas"] = settings["au_eas"]
                        n_type[dev["nu_uuid"]]["au_cal"] = settings["au_cal"]
                        n_type[dev["nu_uuid"]]["au_time"] = settings["au_time"]
                        n_type[dev["nu_uuid"]]["au_all"] = settings["au_all"]

                        if dev["nu_uuid"].endswith(C.PostFix.NATIVE_POSTFIX):
                            #: Native 제품 로그인시 설정 초기화
                            if "au_board" in dev["nu_data"]:
                                n_type[dev["nu_uuid"]]["au_board"] = dev["nu_data"][
                                    "au_board"
                                ]
                        else:

                            #: 사용자API 확인
                            if "nu_hook_curl" in dev:
                                n_type[dev["nu_uuid"]]["au_hook_curl"] = dev[
                                    "nu_hook_curl"
                                ]

                user = {"deviceInfo": n_type}
                conn.hmset(USER_KEY + email, user)
                resp = _resp.Resp(C.ResponseCode.SUCCESS)
            except AttributeError as ae:
                resp = _resp.Resp(C.ResponseCode.FIELD_INVALID)
                raise UserRedisModelException(str(ae))
            except Exception as e:
                resp = _resp.Resp(C.ResponseCode.USER_DB_HANDLING)
                raise UserRedisModelException(str(e))
            finally:
                return resp


if __name__ == "__main__":
    urm = UserRedisModel()
