#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.helpers import utils, responser, log_maker, validator

from v2.databases.db_redis import RDConnector

import ast


""" UserRedisModel (사용자 데이터 처리기)
- 사용자 데이터 처리
"""

_rd = RDConnector()

#: 사용자 정보 키
USER_KEY = C.RedisKey.NOTI_USER

# Responser
_resp = responser.Responser()


class UserRedisModelException(Exception):

    def __init__(self, msg=''):
        self.msg = msg
        log_maker.logging_default(log_type = C.Logger.MD_USER_REDIS, msg = str(msg))

    def __str__(self):
        return self.msg


class UserRedisModel:
    def __init__(self):
        pass

    def get_device_info(self, an_email):
        """ 기기정보 가져오기"""
        if validator.data_is_empty(an_email):
            return False

        conn = _rd.connection

        if conn:
            settings = {}
            token_list = {}
            lists = utils.hget_to_json(conn.hgetall(USER_KEY + an_email))

            if lists:
                device_str = lists[C.DEVICEINFO]
                devices = ast.literal_eval(device_str)

                for device in devices:
                    token_list[device] = devices[device]

            return token_list

    def put_user(self, an_email, data, raw_data=None):
        """ 사용자 저장
        - 로그인 후, 기기데이터 저장
        - PSQL 삽입후, 삽입데이터 토대로 Redis정보 재갱신
        """
        result = False
        if data:
            self.del_user(an_email)
            result = self.insert_redis_data(an_email, data, raw_data)

        return result

    def replace_user_email(self, domain, ch_email, data):
        """ 사용자 이메일내의 도메인변경
        - PSQL 삽입후, 삽입데이터 토대로 Redis정보 재갱신
        """
        result = False
        if data:
            self.del_user_with_domain(domain)
            result = self.insert_redis_data(ch_email, data)

        return result


if __name__ == "__main__":
    urm = UserRedisModel()  
