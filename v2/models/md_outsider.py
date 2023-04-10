#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.databases.db_psql import PGConnector
from v2.databases.db_redis import RDConnector
from v2.helpers import log_maker, utils, validator

""" 웹훅 알림 등록
Jandi등 유사 웹훅서비스가 존재하면 본 프로그램에 수신주소를 등록할 수 있다.
반대로 웹훅을  삭제할 수 있다.
"""

_pg = PGConnector()
_rd = RDConnector()

#: 웹훅키
WEBHOOK_KEY = C.RedisKey.NOTI_WEBHOOK

#: 큐이름
NOTI_QUEUE_MAIL = C.RedisKey.NOTI_QUEUE_MAIL


class OutsiderModelException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.MD_OUTSIDER, msg=str(msg))

    def __str__(self):
        return self.msg


class OutsiderModel:
    def __init__(self):
        pass

    def get_messenger_host(self, email):
        """메신저 호스트 재조회"""
        if validator.data_is_empty(email):
            return False

        try:
            result = _pg.fetch_all(
                """
                SELECT *
                FROM noti 
                WHERE nu_email = '{0}'
                """.format(email)
            )

            if not validator.data_is_empty(result):
                db_res = result

        except Exception as e:
            raise OutsiderModelException(str(e))

        db_res = []

        try:
            result = _pg.fetch_all(
                """
                SELECT nu_data
                FROM user 
                WHERE nu_email = '{0}'
                """.format(email)
            )

            if not validator.data_is_empty(result):
                db_res = result

        except Exception as e:
            raise OutsiderModelException(str(e))

        return db_res

    def get_webhook(self, email):
        """웹훅 도메인 정보 가져오기"""
        if validator.data_is_empty(email):
            return False

        conn = _rd.connection

        if conn:
            try:
                hook_res = {}
                domain = utils.split_text(email, "@", 1) if "@" in email else email

                hook_info = utils.hget_to_json(conn.hgetall(WEBHOOK_KEY + domain))

                names = []
                if hook_info:
                    for _key, _val in hook_info.items():
                        names.append(_key)
                        hook_arr = utils.split_text(_val, "||", -1)
                        hook_res[_key] = {
                            "au_hook_curl": hook_arr[0],
                            "au_host": hook_arr[1],
                        }

                    hook_res["names"] = names

                return hook_res

            except Exception as e:
                raise OutsiderModelException(str(e))

    def post_webhook(self, hook_data):
        """웹훅 도메인 저장 및 수정"""
        if validator.data_is_empty(hook_data):
            return False

        conn = _rd.connection

        if conn:
            try:
                wh_token = hook_data["wh_token"]
                wh_domain = hook_data["wh_dom"]
                wh_curl = hook_data["wh_curl"]
                wh_host = hook_data["wh_host"]

                hook_key = self.get_webhook(wh_domain)

                if hook_key:
                    token_arr = utils.split_text(wh_token, "_", -1)
                    new_token = token_arr[-1]
                    for k, _hook in enumerate(hook_key["names"]):
                        hook_arr = _hook.split("_")

                        if hook_arr[-1] == new_token:
                            del_data = {"wh_dom": wh_domain, "wh_uuid": _hook}

                            self.delete_webhook(del_data, conn)

                redis_hook = {wh_token: "{0}||{1}".format(wh_curl, wh_host)}
                conn.hmset(WEBHOOK_KEY + wh_domain, redis_hook)
            except Exception as e:
                raise OutsiderModelException(str(e))

    def delete_webhook(self, hook_data, conn=None):
        """웹훅 도메인 삭제"""
        if validator.data_is_empty(hook_data):
            return False

        if not conn:
            conn = _rd.connection

        if conn:
            try:
                wh_uuid = hook_data["wh_uuid"]
                wh_domain = hook_data["wh_dom"]

                conn.hdel(WEBHOOK_KEY + wh_domain, wh_uuid)
            except Exception as e:
                raise OutsiderModelException(str(e))


if __name__ == "__main__":
    om = OutsiderModel()
