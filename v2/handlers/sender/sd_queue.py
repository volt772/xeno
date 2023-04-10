#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ast

from v2 import const as C
from v2.databases.db_redis import RDConnector
from v2.helpers import config_loader as _cf
from v2.helpers import log_maker, validator

""" 큐 처리기
Redis 에 저장된 큐를 가져온다
"""

_rd = RDConnector()

#: 큐(메일)
NOTI_QUEUE_MAIL = C.RedisKey.NOTI_QUEUE_MAIL

#: 큐(메일 외)
NOTI_QUEUE_EXTRAS = C.RedisKey.NOTI_QUEUE_EXTRAS

#: 큐(커스텀명령)
NOTI_QUEUE_PROMPT = C.RedisKey.NOTI_QUEUE_PROMPT


class SenderQueueException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.SD_QUEUE, msg=str(msg))

    def __str__(self):
        return self.msg


class SenderQueue:
    def __init__(self):
        #: 큐 Bulk Select 사이즈
        size = _cf.get_config(C.ConfigKey.QUEUE)[C.ConfigValue.POP_SIZE]
        self.pop_size = int(size)

    def put_exception_data(self, data):
        """실패데이터 다시 밀어넣기"""
        if validator.data_is_empty(data):
            return False

        conn = _rd.connection
        conn.rpush(NOTI_QUEUE_MAIL, data)

    def multi_pop(self, r, q, n):
        """다중 lpop"""
        p = r.pipeline()
        p.multi()
        p.lrange(q, 0, n - 1)
        p.ltrim(q, n, -1)

        return p.execute()

    def get_notidata(self, q_type="mail"):
        """메일발송데이터 가져오기"""
        conn = _rd.connection

        noti_data = []

        r_data = None
        if q_type == "mail":
            r_data = self.multi_pop(conn, NOTI_QUEUE_MAIL, self.pop_size)
        else:
            queue_name = NOTI_QUEUE_PROMPT if q_type == "prompts" else NOTI_QUEUE_EXTRAS

            extra_pop_size = int(self.pop_size / 2)
            if extra_pop_size > 0:
                r_data = self.multi_pop(conn, queue_name, extra_pop_size)

        try:
            if not validator.data_is_empty(r_data):
                queues = r_data[0]
                for q in queues:
                    ucc_type = (
                        "unicode-escape" if "mailplug_notify_v1" in str(q) else "utf-8"
                    )
                    noti_data.append(self.arrange_notidata(q.decode(ucc_type)))
        except Exception as e:
            raise SenderQueueException(str(e))

        return noti_data

    def arrange_notidata(self, r_data):
        """메일발송데이터 정리"""
        noti_data = []
        try:
            if not validator.data_is_empty(r_data):
                noti_data = ast.literal_eval(r_data)
        except Exception as e:
            raise SenderQueueException(str(e))

        return noti_data


if __name__ == "__main__":
    sq = SenderQueue()
