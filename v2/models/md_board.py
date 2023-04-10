#!/usr/bin/python3
# -*- coding: utf-8 -*-

from v2 import const as C
from v2.databases.db_redis import RDConnector
from v2.helpers import log_maker, validator

""" 게시판 알림 저장
새글, 댓글, 대댓글등 게시판에 관련된 액션이 발생하면,
알림서버에서 정보 수신 및 Redis에 큐로 적재한다.
"""

_rd = RDConnector()

#: 큐이름
_Q = C.RedisKey.NOTI_QUEUE_EXTRAS


class BoardModelException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        log_maker.logging_default(log_type=C.Logger.MD_BOARD, msg=str(msg))

    def __str__(self):
        return self.msg


class BoardModel:
    def __init__(self):
        self.conn = None

    def post_board(self, bq_list):
        """게시판 데이터 저장"""
        if validator.data_is_empty(bq_list):
            return False

        #: Get Connection
        if not self.conn:
            self.conn = _rd.connection

        #: 큐 삽입
        if self.conn:
            try:
                for _bq in bq_list:
                    self.conn.rpush(_Q, _bq)
            except Exception as e:
                raise BoardModelException(str(e))


if __name__ == "__main__":
    bm = BoardModel()
