#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.databases.db_redis import RDConnector
from v2.helpers import log_maker, utils, validator

""" 메일 알림 저장
이메일 수신시 '보낸사람, 제목'으로 구성된 알림데이터 수신하면 
Redis에 큐로 적재한다.
"""

_rd = RDConnector()

#: 큐이름
NOTI_QUEUE_MAIL = C.RedisKey.NOTI_QUEUE_MAIL

#: 호스트정보 키
MAILINFO_KEY = C.RedisKey.MAIL_INFO


class MailModelException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.MD_MAIL, msg=str(msg))

    def __str__(self):
        return self.msg


class MailModel:
    def __init__(self):
        pass

    def put_noti(self, data):
        """메일발송데이터 저장"""
        conn = _rd.connection

        if conn and data:
            an_email = data.get("to", "")

            if validator.data_is_empty(an_email):
                return False

            #: 데이터 Delay시간 검사용 Time
            saved_time = utils.get_current_time()

            try:
                n_data = {
                    "type": data.get("type", ""),
                    "from": data.get("from", ""),
                    "to": data.get("to", ""),
                    "kind": data.get("kind", ""),
                    "subject": data.get("subject", ""),
                    "content": data.get("content", ""),
                }

                conn.rpush(NOTI_QUEUE_MAIL, n_data)
            except Exception:
                return False


if __name__ == "__main__":
    mm = MailModel()
